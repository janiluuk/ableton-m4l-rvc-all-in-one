// rvc_unified.js
// One Node-for-Max client that supports two backends:
// - Replicate (cloud) via replicate SDK
// - Local FastAPI server via HTTP POST /convert
const Max = require('max-api');
const fs = require('fs/promises');
const path = require('path');
const os = require('os');
const fetch = require('node-fetch');
const FormData = require('form-data');
const Replicate = require('replicate');
const AdmZip = require('adm-zip');

// Optional client-side normalization for Replicate WAV (same as before)
const audioDecode = require('audio-decode');
const WavEncoder = require('wav-encoder');

// Optional local Stable Audio transform endpoint: trigger with the `stable_process` message
// to send the most recent source audio plus optional prompt.

let state = {
  backend: 'Replicate',           // 'Replicate' or 'Local'
  mode: 'voice',                  // 'voice' (RVC) or 'stable'
  apikey: null,                   // Replicate
  server: 'http://127.0.0.1:8000',// Local
  stability_server: 'http://127.0.0.1:7860',
  stable_prompt: '',
  uvr_model: 'htdemucs',
  uvr_shifts: 1,
  uvr_segment: 0,
  sourcePath: null,

  // Shared params
  rvc_model: null,
  model_url: null,                // only for Replicate model that accepts URL
  output_format: 'wav',
  pitch_change: 'no-change',      // deprecated in some models (Replicate)
  index_rate: 0.5,
  filter_radius: 3,
  rms_mix_rate: 0.25,
  pitch_detection_algorithm: 'rmvpe',
  crepe_hop_length: 128,
  protect: 0.33,
  main_vocals_volume_change: 0,
  backup_vocals_volume_change: 0,
  instrumental_volume_change: 0,
  pitch_change_all: 0,            // <-- key pitch control
  // Local extras
  separate: false,
  stem: 'vocals',
  // Applio params
  applio_enabled: false,
  applio_model: null,
  // Normalization
  normalize: true,
  target_db: -0.1
};

function status(s){ Max.outlet(['status', s]); }
function progress(p){ Max.outlet(['progress', p]); }
function errorOut(e){ Max.outlet(['error', e]); }

// Handlers
Max.addHandler('backend', v => { state.backend = String(v || 'Replicate'); status(`Backend: ${state.backend}`); });
Max.addHandler('mode', v => {
  const val = String(v || 'voice').toLowerCase();
  if (val.includes('uvr')) {
    state.mode = 'uvr';
  } else if (val.startsWith('stable')) {
    state.mode = 'stable';
  } else {
    state.mode = 'voice';
  }
  status(`Mode: ${state.mode}`);
});
Max.addHandler('apikey', v => { state.apikey = String(v || '').trim(); status('API key set'); });
Max.addHandler('server', v => { state.server = String(v || '').trim(); status(`Server: ${state.server}`); });
Max.addHandler('source', v => { state.sourcePath = String(v || '').trim(); status(`Source: ${state.sourcePath}`); });
Max.addHandler('stability_server', v => {
  state.stability_server = String(v || '').trim() || 'http://127.0.0.1:7860';
  status(`Stable Audio server: ${state.stability_server}`);
});
Max.addHandler('stable_prompt', v => {
  state.stable_prompt = (v==null?'':String(v)).trim();
  status(`stable_prompt=${state.stable_prompt}`);
});
Max.addHandler('uvr_model', v => {
  state.uvr_model = (v==null?'':String(v)).trim() || 'htdemucs';
  status(`uvr_model=${state.uvr_model}`);
});

['rvc_model','model_url','output_format','pitch_change','pitch_detection_algorithm','stem','applio_model'].forEach(k=>{
  Max.addHandler(k, v => { state[k] = (v==null?'':String(v)).trim(); status(`${k}=${state[k]}`); });
});

['index_rate','filter_radius','rms_mix_rate','crepe_hop_length','protect',
 'main_vocals_volume_change','backup_vocals_volume_change','instrumental_volume_change',
 'pitch_change_all','target_db','uvr_shifts','uvr_segment']
.forEach(k=>{
  Max.addHandler(k, v => { 
    const num = Number(v);
    if (!Number.isFinite(num)) return errorOut(`Expected number for ${k}`);
    state[k] = num; status(`${k}=${state[k]}`);
  });
});

Max.addHandler('separate', v => { state.separate = !!Number(v) || v === true; status(`separate=${state.separate}`); });
Max.addHandler('normalize', v => { state.normalize = !!Number(v) || v === true; status(`normalize=${state.normalize}`); });
Max.addHandler('applio_enabled', v => { state.applio_enabled = !!Number(v) || v === true; status(`applio_enabled=${state.applio_enabled}`); });

Max.addHandler('process', async () => {
  try {
    if (!state.sourcePath) return errorOut('No source file');
    const mode = (state.mode || 'voice').toLowerCase();
    if (mode.startsWith('stable')) {
      await runStableAudio();
    } else if (mode.startsWith('uvr')) {
      await runUvr();
    } else {
      const backend = state.backend.toLowerCase();
      if (backend.startsWith('rep')) {
        if (!state.apikey) return errorOut('Missing Replicate API key');
        await runReplicate();
      } else {
        await runLocal();
      }
    }
  } catch (err) {
    errorOut(err?.message || String(err));
  }
});

Max.addHandler('stable_process', async () => {
  try {
    if (!state.sourcePath) return errorOut('No source file');
    await runStableAudio();
  } catch (err) {
    errorOut(err?.message || String(err));
  }
});

async function listAudioFiles(dir){
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const results = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...await listAudioFiles(full));
    } else if (/\.(wav|mp3|flac|ogg)$/i.test(entry.name)) {
      results.push(full);
    }
  }
  return results;
}

async function runReplicate() {
  const buf = await fs.readFile(state.sourcePath);
  status('Starting job (Replicate)…');
  const replicate = new Replicate({ auth: state.apikey });
  const input = {
    song_input: buf,
    output_format: state.output_format,
    pitch_change: state.pitch_change,  // model-specific
    index_rate: state.index_rate,
    filter_radius: state.filter_radius,
    rms_mix_rate: state.rms_mix_rate,
    pitch_detection_algorithm: state.pitch_detection_algorithm,
    crepe_hop_length: state.crepe_hop_length,
    protect: state.protect,
    main_vocals_volume_change: state.main_vocals_volume_change,
    backup_vocals_volume_change: state.backup_vocals_volume_change,
    instrumental_volume_change: state.instrumental_volume_change,
    pitch_change_all: state.pitch_change_all
  };
  if (state.model_url) input.custom_rvc_model_download_url = state.model_url;
  if (state.rvc_model) input.rvc_model = state.rvc_model;

  const modelSlug = "zsxkib/realistic-voice-cloning";
  const out = await replicate.run(modelSlug, { input });
  if (!out) throw new Error('No output from model');
  const outUrl = Array.isArray(out) ? out[0] : out;

  status('Downloading result…');
  const res = await fetch(outUrl);
  if (!res.ok) throw new Error(`Download failed: ${res.status}`);
  const dir = path.join(os.homedir(), 'Music', 'RVC');
  await fs.mkdir(dir, { recursive: true });
  const ext = state.output_format === 'wav' ? 'wav' : 'mp3';
  const outPath = path.join(dir, `rvc_${Date.now()}.${ext}`);
  const file = await fs.open(outPath, 'w');
  await res.body.pipeTo(file.createWriteStream());
  await file.close();

  if (state.normalize && ext === 'wav') {
    status('Normalizing audio…');
    try {
      await normalizeWav(outPath, state.target_db);
      status(`Normalized to ${state.target_db} dBFS`);
    } catch (e) {
      errorOut('Normalization failed: ' + (e?.message || e));
    }
  }
  progress(100);
  status('Done');
  Max.outlet(['done', outPath]);
}

async function runLocal() {
  const form = new FormData();
  form.append('file', await fs.readFile(state.sourcePath), { filename: path.basename(state.sourcePath) });
  const map = ['rvc_model','output_format','index_rate','filter_radius','rms_mix_rate',
               'pitch_detection_algorithm','crepe_hop_length','protect',
               'main_vocals_volume_change','backup_vocals_volume_change','instrumental_volume_change',
               'pitch_change_all','normalize','target_db','separate','stem',
               'applio_enabled','applio_model'];
  for (const k of map) form.append(k, String(state[k]));
  if (state.uvr_model) form.append('demucs_model', state.uvr_model);
  status(`Uploading to ${state.server}…`);
  const res = await fetch(`${state.server}/convert`, { method: 'POST', body: form });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Server error: ${res.status} ${txt}`);
  }
  
  const dir = path.join(os.homedir(), 'Music', 'RVC');
  await fs.mkdir(dir, { recursive: true });
  
  const ct = res.headers.get('content-type') || '';
  
  // Check if response is a zip file (Applio enabled)
  if (ct.includes('application/zip')) {
    const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'rvc-applio-'));
    const zipPath = path.join(tmpDir, 'outputs.zip');
    const zipFile = await fs.open(zipPath, 'w');
    await res.body.pipeTo(zipFile.createWriteStream());
    await zipFile.close();

    const outDir = path.join(dir, `rvc_applio_${Date.now()}`);
    await fs.mkdir(outDir, { recursive: true });
    const zip = new AdmZip(zipPath);
    zip.extractAllTo(outDir, true);

    const outputs = await listAudioFiles(outDir);
    if (!outputs.length) throw new Error('Zip contained no audio files');
    
    for (const output of outputs) {
      Max.outlet(['done', output]);
      status(`Output: ${path.basename(output)}`);
    }
    status(`Both RVC and Applio outputs ready in ${outDir}`);
  } else {
    // Single file response (no Applio)
    const ext = ct.includes('mpeg') ? 'mp3' : 'wav';
    const outPath = path.join(dir, `rvc_${Date.now()}.${ext}`);
    const file = await fs.open(outPath, 'w');
    await res.body.pipeTo(file.createWriteStream());
    await file.close();
    Max.outlet(['done', outPath]);
    status(`Output: ${outPath}`);
  }
  
  progress(100);
  status('Done');
}

async function runUvr() {
  const form = new FormData();
  form.append('file', await fs.readFile(state.sourcePath), { filename: path.basename(state.sourcePath) });
  if (state.uvr_model) form.append('model', state.uvr_model);
  if (Number.isFinite(state.uvr_shifts)) form.append('shifts', String(state.uvr_shifts));
  if (Number.isFinite(state.uvr_segment) && state.uvr_segment > 0) form.append('segment', String(state.uvr_segment));
  status(`Uploading to UVR at ${state.server}…`);
  const res = await fetch(`${state.server}/uvr`, { method: 'POST', body: form });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`UVR server error: ${res.status} ${txt}`);
  }

  const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'uvr-'));
  const zipPath = path.join(tmpDir, 'uvr.zip');
  const zipFile = await fs.open(zipPath, 'w');
  await res.body.pipeTo(zipFile.createWriteStream());
  await zipFile.close();

  const outDir = path.join(os.homedir(), 'Music', 'RVC', `uvr_${Date.now()}`);
  await fs.mkdir(outDir, { recursive: true });
  const zip = new AdmZip(zipPath);
  zip.extractAllTo(outDir, true);

  const stems = await listAudioFiles(outDir);
  if (!stems.length) throw new Error('UVR zip contained no audio stems');
  let i = 0;
  for (const stem of stems) {
    progress(Math.min(99, Math.round((++i / stems.length) * 100)));
    Max.outlet(['done', stem]);
  }
  progress(100);
  status(`UVR stems ready in ${outDir}`);
}

async function runStableAudio() {
  const buf = await fs.readFile(state.sourcePath);
  const form = new FormData();
  form.append('input_audio', buf, { filename: path.basename(state.sourcePath) });
  if (state.stable_prompt) form.append('prompt', state.stable_prompt);
  form.append('output_format', state.output_format || 'wav');

  const base = (state.stability_server || 'http://127.0.0.1:7860').replace(/\/+$/, '');
  status(`Uploading to ${base}…`);
  const res = await fetch(`${base}/v2beta/stable-audio/transform`, {
    method: 'POST',
    headers: { Accept: 'audio/*' },
    body: form
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Stable Audio error: ${res.status} ${txt}`);
  }

  const dir = path.join(os.homedir(), 'Music', 'RVC');
  await fs.mkdir(dir, { recursive: true });
  const ct = res.headers.get('content-type') || '';
  const ext = ct.includes('mpeg') ? 'mp3' : (ct.includes('ogg') ? 'ogg' : 'wav');
  const outPath = path.join(dir, `rvc_${Date.now()}.${ext}`);
  const file = await fs.open(outPath, 'w');
  await res.body.pipeTo(file.createWriteStream());
  await file.close();

  if (state.normalize && ext === 'wav') {
    status('Normalizing audio…');
    try {
      await normalizeWav(outPath, state.target_db);
      status(`Normalized to ${state.target_db} dBFS`);
    } catch (e) {
      errorOut('Normalization failed: ' + (e?.message || e));
    }
  }

  progress(100);
  status('Done');
  Max.outlet(['done', outPath]);
}

async function normalizeWav(filePath, targetDb = -0.1) {
  const buf = await fs.readFile(filePath);
  const audioBuffer = await audioDecode(buf);
  let maxSample = 0;
  for (let c = 0; c < audioBuffer.numberOfChannels; c++) {
    const channelData = audioBuffer.getChannelData(c);
    for (let i = 0; i < channelData.length; i++) {
      const v = Math.abs(channelData[i]);
      if (v > maxSample) maxSample = v;
    }
  }
  if (maxSample === 0) return;
  const targetAmp = Math.pow(10, targetDb / 20);
  const g = targetAmp / maxSample;
  for (let c = 0; c < audioBuffer.numberOfChannels; c++) {
    const channelData = audioBuffer.getChannelData(c);
    for (let i = 0; i < channelData.length; i++) channelData[i] *= g;
  }
  const encoded = await WavEncoder.encode({
    sampleRate: audioBuffer.sampleRate,
    channelData: Array.from({length: audioBuffer.numberOfChannels}, (_, c) => audioBuffer.getChannelData(c))
  });
  await fs.writeFile(filePath, Buffer.from(encoded));
}

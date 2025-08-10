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

// Optional client-side normalization for Replicate WAV (same as before)
const audioDecode = require('audio-decode');
const WavEncoder = require('wav-encoder');

let state = {
  backend: 'Replicate',           // 'Replicate' or 'Local'
  apikey: null,                   // Replicate
  server: 'http://127.0.0.1:8000',// Local
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
  // Normalization
  normalize: true,
  target_db: -0.1
};

function status(s){ Max.outlet(['status', s]); }
function progress(p){ Max.outlet(['progress', p]); }
function errorOut(e){ Max.outlet(['error', e]); }

// Handlers
Max.addHandler('backend', v => { state.backend = String(v || 'Replicate'); status(`Backend: ${state.backend}`); });
Max.addHandler('apikey', v => { state.apikey = String(v || '').trim(); status('API key set'); });
Max.addHandler('server', v => { state.server = String(v || '').trim(); status(`Server: ${state.server}`); });
Max.addHandler('source', v => { state.sourcePath = String(v || '').trim(); status(`Source: ${state.sourcePath}`); });

['rvc_model','model_url','output_format','pitch_change','pitch_detection_algorithm','stem'].forEach(k=>{
  Max.addHandler(k, v => { state[k] = (v==null?'':String(v)).trim(); status(`${k}=${state[k]}`); });
});

['index_rate','filter_radius','rms_mix_rate','crepe_hop_length','protect',
 'main_vocals_volume_change','backup_vocals_volume_change','instrumental_volume_change',
 'pitch_change_all','target_db']
.forEach(k=>{
  Max.addHandler(k, v => { 
    const num = Number(v);
    if (!Number.isFinite(num)) return errorOut(`Expected number for ${k}`);
    state[k] = num; status(`${k}=${state[k]}`);
  });
});

Max.addHandler('separate', v => { state.separate = !!Number(v) || v === true; status(`separate=${state.separate}`); });
Max.addHandler('normalize', v => { state.normalize = !!Number(v) || v === true; status(`normalize=${state.normalize}`); });

Max.addHandler('process', async () => {
  try {
    if (!state.sourcePath) return errorOut('No source file');
    if (state.backend.toLowerCase().startsWith('rep')) {
      if (!state.apikey) return errorOut('Missing Replicate API key');
      await runReplicate();
    } else {
      await runLocal();
    }
  } catch (err) {
    errorOut(err?.message || String(err));
  }
});

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
               'pitch_change_all','normalize','target_db','separate','stem'];
  for (const k of map) form.append(k, String(state[k]));
  status(`Uploading to ${state.server}…`);
  const res = await fetch(`${state.server}/convert`, { method: 'POST', body: form });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Server error: ${res.status} ${txt}`);
  }
  const dir = path.join(os.homedir(), 'Music', 'RVC');
  await fs.mkdir(dir, { recursive: true });
  const ct = res.headers.get('content-type') || '';
  const ext = ct.includes('mpeg') ? 'mp3' : 'wav';
  const outPath = path.join(dir, `rvc_${Date.now()}.${ext}`);
  const file = await fs.open(outPath, 'w');
  await res.body.pipeTo(file.createWriteStream());
  await file.close();
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

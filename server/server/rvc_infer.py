# server/rvc_infer.py
import os, tempfile, subprocess, contextlib, wave, numpy as np, shutil
import torch, warnings, librosa, importlib, hashlib, math
from scipy.io import wavfile
warnings.filterwarnings("ignore")

def peak_normalize_wav(path, target_db=-0.1):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        audio = wf.readframes(n_frames)
    if sampwidth != 2:
        return
    samples = np.frombuffer(audio, dtype=np.int16).astype(np.float32)
    peak = np.max(np.abs(samples)) / 32768.0
    if peak == 0:
        return
    target_amp = 10 ** (target_db / 20.0)
    gain = target_amp / peak
    samples = np.clip(samples * gain, -32768, 32767).astype(np.int16)
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(2)
        wf.setframerate(framerate)
        wf.writeframes(samples.tobytes())

def demucs_run(in_path, model=None, shifts=None, segment=None):
    """Run Demucs once and return the output directory containing all stems."""
    tmp_out = tempfile.mkdtemp()
    model_name = model or os.environ.get("DEMUCS_MODEL", "htdemucs")
    cmd = ["demucs", "-n", model_name, "-o", tmp_out, in_path]
    if shifts is not None:
        try:
            s = int(shifts)
            if s > 0:
                cmd += ["--shifts", str(s)]
        except (TypeError, ValueError):
            pass
    if segment is not None:
        try:
            seg = float(segment)
            if seg > 0:
                cmd += ["--segment", str(seg)]
        except (TypeError, ValueError):
            pass
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    base = os.path.splitext(os.path.basename(in_path))[0]
    out_dir = os.path.join(tmp_out, model_name, base)
    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"Demucs output directory missing: {out_dir}")
    return out_dir


def demucs_separate(in_path, stem='vocals', model=None, shifts=None, segment=None):
    """Run Demucs (htdemucs) and return path to requested stem wav."""
    out_dir = demucs_run(in_path, model=model, shifts=shifts, segment=segment)
    stem_name = "vocals" if stem not in ["drums","bass","other"] else stem
    stem_path = os.path.join(out_dir, f"{stem_name}.wav")
    if not os.path.exists(stem_path):
        raise FileNotFoundError(f"Demucs stem not found: {stem_path}")
    return stem_path, out_dir


class UVRSeparator:
    """Ultimate Vocal Remover separator using uvr5_pack library."""
    
    def __init__(self, model_path=None, device=None, is_half=True):
        from uvr5_pack.lib_v5 import spec_utils
        from uvr5_pack.utils import _get_name_params, inference
        from uvr5_pack.lib_v5.model_param_init import ModelParameters
        
        self.model_path = model_path or os.environ.get("UVR_MODEL_PATH", "/uvr5_weights/2_HP-UVR.pth")
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.is_half = is_half and self.device == 'cuda'
        
        self.data = {
            'postprocess': False,
            'tta': False,
            'window_size': 512,
            'agg': 10,
            'high_end_process': 'mirroring',
        }
        
        nn_arch_sizes = [31191, 33966, 61968, 123821, 123812, 537238]
        model_size = math.ceil(os.stat(self.model_path).st_size / 1024)
        nn_architecture = '{}KB'.format(min(nn_arch_sizes, key=lambda x: abs(x - model_size)))
        
        nets = importlib.import_module(
            'uvr5_pack.lib_v5.nets' + f'_{nn_architecture}'.replace('_{}KB'.format(nn_arch_sizes[0]), ''),
            package=None
        )
        
        model_hash = hashlib.md5(open(self.model_path, 'rb').read()).hexdigest()
        param_name, model_params_d = _get_name_params(self.model_path, model_hash)
        
        mp = ModelParameters(model_params_d)
        model = nets.CascadedASPPNet(mp.param['bins'] * 2)
        cpk = torch.load(self.model_path, map_location='cpu')
        model.load_state_dict(cpk)
        model.eval()
        
        if self.is_half:
            model = model.half().to(self.device)
        else:
            model = model.to(self.device)
        
        self.mp = mp
        self.model = model
    
    def separate(self, music_file, vocal_path=None, instrument_path=None):
        """Separate audio into vocals and instruments."""
        from uvr5_pack.lib_v5 import spec_utils
        from uvr5_pack.utils import inference
        
        if vocal_path is None and instrument_path is None:
            raise ValueError("At least one output path must be specified")
        
        # Create output directories
        if vocal_path:
            os.makedirs(os.path.dirname(vocal_path), exist_ok=True)
        if instrument_path:
            os.makedirs(os.path.dirname(instrument_path), exist_ok=True)
        
        X_wave, X_spec_s = {}, {}
        bands_n = len(self.mp.param['band'])
        
        for d in range(bands_n, 0, -1):
            bp = self.mp.param['band'][d]
            if d == bands_n:
                X_wave[d], _ = librosa.core.load(
                    music_file, bp['sr'], False, dtype=np.float32, res_type=bp['res_type']
                )
                if X_wave[d].ndim == 1:
                    X_wave[d] = np.asfortranarray([X_wave[d], X_wave[d]])
            else:
                X_wave[d] = librosa.core.resample(
                    X_wave[d + 1], self.mp.param['band'][d + 1]['sr'], bp['sr'], res_type=bp['res_type']
                )
            
            X_spec_s[d] = spec_utils.wave_to_spectrogram_mt(
                X_wave[d], bp['hl'], bp['n_fft'], self.mp.param['mid_side'],
                self.mp.param['mid_side_b2'], self.mp.param['reverse']
            )
            
            if d == bands_n and self.data['high_end_process'] != 'none':
                input_high_end_h = (bp['n_fft'] // 2 - bp['crop_stop']) + (
                    self.mp.param['pre_filter_stop'] - self.mp.param['pre_filter_start']
                )
                input_high_end = X_spec_s[d][:, bp['n_fft'] // 2 - input_high_end_h:bp['n_fft'] // 2, :]
        
        X_spec_m = spec_utils.combine_spectrograms(X_spec_s, self.mp)
        aggresive_set = float(self.data['agg'] / 100)
        aggressiveness = {'value': aggresive_set, 'split_bin': self.mp.param['band'][1]['crop_stop']}
        
        with torch.no_grad():
            pred, X_mag, X_phase = inference(X_spec_m, self.device, self.model, aggressiveness, self.data)
        
        if self.data['postprocess']:
            pred_inv = np.clip(X_mag - pred, 0, np.inf)
            pred = spec_utils.mask_silence(pred, pred_inv)
        
        y_spec_m = pred * X_phase
        v_spec_m = X_spec_m - y_spec_m
        
        if instrument_path:
            if self.data['high_end_process'].startswith('mirroring'):
                input_high_end_ = spec_utils.mirroring(
                    self.data['high_end_process'], y_spec_m, input_high_end, self.mp
                )
                wav_instrument = spec_utils.cmb_spectrogram_to_wave(
                    y_spec_m, self.mp, input_high_end_h, input_high_end_
                )
            else:
                wav_instrument = spec_utils.cmb_spectrogram_to_wave(y_spec_m, self.mp)
            
            wavfile.write(
                instrument_path, self.mp.param['sr'],
                (np.array(wav_instrument) * 32768).astype("int16")
            )
        
        if vocal_path:
            if self.data['high_end_process'].startswith('mirroring'):
                input_high_end_ = spec_utils.mirroring(
                    self.data['high_end_process'], v_spec_m, input_high_end, self.mp
                )
                wav_vocals = spec_utils.cmb_spectrogram_to_wave(
                    v_spec_m, self.mp, input_high_end_h, input_high_end_
                )
            else:
                wav_vocals = spec_utils.cmb_spectrogram_to_wave(v_spec_m, self.mp)
            
            wavfile.write(
                vocal_path, self.mp.param['sr'],
                (np.array(wav_vocals) * 32768).astype("int16")
            )
        
        return vocal_path, instrument_path


def uvr_separate(in_path, stem='vocals', model_path=None):
    """Run UVR separation and return path to requested stem wav."""
    tmp_out = tempfile.mkdtemp()
    separator = UVRSeparator(model_path=model_path)
    
    vocal_path = os.path.join(tmp_out, "vocals.wav")
    instrument_path = os.path.join(tmp_out, "instrument.wav")
    
    separator.separate(in_path, vocal_path=vocal_path, instrument_path=instrument_path)
    
    if stem == 'vocals':
        if not os.path.exists(vocal_path):
            raise FileNotFoundError(f"UVR vocal stem not found: {vocal_path}")
        return vocal_path, tmp_out
    else:
        if not os.path.exists(instrument_path):
            raise FileNotFoundError(f"UVR instrument stem not found: {instrument_path}")
        return instrument_path, tmp_out

class RVCConverter:
    def __init__(self):
        self.paths = {
            "webui_cli": "/rvc/infer_cli.py",
            "mangio": "/rvc/inference.py",
        }

    def _webui_call(self, in_path, out_path, **kw):
        args = ["python", self.paths["webui_cli"],
                "--input", in_path,
                "--output", out_path]
        voice = kw.get("rvc_model")
        if voice:
            mdir = os.path.join("/models", voice)
            mp = os.path.join(mdir, "model.pth")
            ix = os.path.join(mdir, "added.index")
            if os.path.exists(mp):
                args += ["--model", mp]
            if os.path.exists(ix):
                args += ["--index", ix]
        if kw.get("pitch_change_all") is not None:
            args += ["--transpose", str(kw["pitch_change_all"])]
        if kw.get("index_rate") is not None:
            args += ["--index-rate", str(kw["index_rate"])]
        if kw.get("filter_radius") is not None:
            args += ["--filter-radius", str(kw["filter_radius"])]
        if kw.get("rms_mix_rate") is not None:
            args += ["--rms-mix-rate", str(kw["rms_mix_rate"])]
        if kw.get("pitch_detection_algorithm"):
            args += ["--f0-method", str(kw["pitch_detection_algorithm"])]
        return args

    def _mangio_call(self, in_path, out_path, **kw):
        args = ["python", self.paths["mangio"],
                "--input_path", in_path,
                "--output_path", out_path]
        voice = kw.get("rvc_model")
        if voice:
            mdir = os.path.join("/models", voice)
            mp = os.path.join(mdir, "model.pth")
            ix = os.path.join(mdir, "added.index")
            if os.path.exists(mp):
                args += ["--pth_path", mp]
            if os.path.exists(ix):
                args += ["--index_path", ix]
        if kw.get("pitch_change_all") is not None:
            args += ["--transpose", str(kw["pitch_change_all"])]
        if kw.get("index_rate") is not None:
            args += ["--index_rate", str(kw["index_rate"])]
        if kw.get("filter_radius") is not None:
            args += ["--filter_radius", str(kw["filter_radius"])]
        if kw.get("rms_mix_rate") is not None:
            args += ["--rms_mix_rate", str(kw["rms_mix_rate"])]
        if kw.get("pitch_detection_algorithm"):
            args += ["--f0_method", str(kw["pitch_detection_algorithm"])]
        return args

    def convert(self, **kw):
        in_path = kw["in_path"]
        output_format = kw.get("output_format","wav")
        normalize = kw.get("normalize", True)
        target_db = kw.get("target_db", -0.1)

        work_input = in_path
        if kw.get("separate"):
            separator = kw.get("separator", "demucs")  # Default to demucs for backward compatibility
            stem = kw.get("stem", "vocals")
            
            if separator == "uvr":
                model_path = kw.get("uvr_model_path")
                work_input, _ = uvr_separate(in_path, stem=stem, model_path=model_path)
            else:
                work_input, _ = demucs_separate(in_path, stem=stem, model=kw.get("demucs_model"))

        tmp_dir = tempfile.mkdtemp()
        out_path = os.path.join(tmp_dir, "rvc_out." + ("wav" if output_format=="wav" else "mp3"))

        if os.path.exists(self.paths["webui_cli"]):
            cmd = self._webui_call(work_input, out_path, **kw)
        elif os.path.exists(self.paths["mangio"]):
            cmd = self._mangio_call(work_input, out_path, **kw)
        else:
            raise RuntimeError("No known RVC CLI found in /rvc (expected infer_cli.py or inference.py)")

        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0 or not os.path.exists(out_path):
            raise RuntimeError(f"RVC CLI failed: {proc.stderr or proc.stdout}")

        if normalize and out_path.endswith(".wav"):
            try:
                peak_normalize_wav(out_path, target_db)
            except Exception:
                pass
        return out_path

    def uvr(self, in_path, model=None, shifts=None, segment=None, use_uvr=False, uvr_model_path=None):
        """Separate all stems and return a zip archive path.
        
        Args:
            in_path: Input audio file path
            model: Demucs model name (for backward compatibility)
            shifts: Demucs shifts parameter (for backward compatibility)
            segment: Demucs segment parameter (for backward compatibility)
            use_uvr: If True, use UVR separator instead of Demucs
            uvr_model_path: Path to UVR model weights
        """
        if use_uvr:
            # Use UVR separation
            tmp_out = tempfile.mkdtemp()
            separator = UVRSeparator(model_path=uvr_model_path)
            
            vocal_path = os.path.join(tmp_out, "vocals.wav")
            instrument_path = os.path.join(tmp_out, "instrument.wav")
            
            separator.separate(in_path, vocal_path=vocal_path, instrument_path=instrument_path)
            
            # Create zip archive
            base = tempfile.mktemp()
            archive_path = shutil.make_archive(base, 'zip', tmp_out)
            if not os.path.exists(archive_path):
                raise FileNotFoundError("Failed to create UVR zip archive")
            return archive_path
        else:
            # Use Demucs (original behavior)
            out_dir = demucs_run(in_path, model=model, shifts=shifts, segment=segment)
            base = tempfile.mktemp()
            archive_path = shutil.make_archive(base, 'zip', out_dir)
            if not os.path.exists(archive_path):
                raise FileNotFoundError("Failed to create UVR zip archive")
            return archive_path

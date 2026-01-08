# server/rvc_infer.py
import os, tempfile, subprocess, contextlib, wave, numpy as np, shutil
import urllib.request
import urllib.parse

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

class RVCConverter:
    def __init__(self):
        self.paths = {
            "webui_cli": "/rvc/infer_cli.py",
            "mangio": "/rvc/inference.py",
        }
        # Applio server URL (environment variable or default)
        self.applio_server = os.environ.get("APPLIO_SERVER", "http://applio:8001")

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

    def _process_with_applio(self, vocal_path, **kw):
        """Process separated vocals through Applio container via HTTP and return the output path."""
        import json
        from urllib.error import URLError, HTTPError
        
        output_format = kw.get("output_format", "wav")
        normalize = kw.get("normalize", True)
        target_db = kw.get("target_db", -0.1)

        # Prepare multipart form data
        boundary = '----WebKitFormBoundary' + ''.join([str(ord(c)) for c in os.urandom(8).hex()[:16]])
        
        # Read the audio file
        with open(vocal_path, 'rb') as f:
            audio_data = f.read()
        
        # Build multipart form data
        body = []
        
        # Add file
        body.append(f'--{boundary}'.encode())
        body.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(vocal_path)}"'.encode())
        body.append(b'Content-Type: audio/wav')
        body.append(b'')
        body.append(audio_data)
        
        # Add model_name
        model_name = kw.get("applio_model") if kw.get("applio_model") else kw.get("rvc_model")
        if model_name:
            body.append(f'--{boundary}'.encode())
            body.append(b'Content-Disposition: form-data; name="model_name"')
            body.append(b'')
            body.append(model_name.encode())
        
        # Add pitch
        if kw.get("pitch_change_all") is not None:
            body.append(f'--{boundary}'.encode())
            body.append(b'Content-Disposition: form-data; name="pitch"')
            body.append(b'')
            body.append(str(int(kw["pitch_change_all"])).encode())
        
        # Add other parameters
        params = {
            'index_rate': kw.get("index_rate"),
            'filter_radius': kw.get("filter_radius"),
            'rms_mix_rate': kw.get("rms_mix_rate"),
            'f0_method': kw.get("pitch_detection_algorithm"),
            'output_format': output_format
        }
        
        for param_name, param_value in params.items():
            if param_value is not None:
                body.append(f'--{boundary}'.encode())
                body.append(f'Content-Disposition: form-data; name="{param_name}"'.encode())
                body.append(b'')
                body.append(str(param_value).encode())
        
        body.append(f'--{boundary}--'.encode())
        body_bytes = b'\r\n'.join(body)
        
        # Make HTTP request to Applio container
        try:
            req = urllib.request.Request(
                f"{self.applio_server}/convert",
                data=body_bytes,
                headers={
                    'Content-Type': f'multipart/form-data; boundary={boundary}',
                    'Content-Length': str(len(body_bytes))
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=300) as response:
                if response.status != 200:
                    raise RuntimeError(f"Applio server returned status {response.status}")
                
                # Save response to file
                tmp_dir = tempfile.mkdtemp()
                applio_out = os.path.join(tmp_dir, "applio_out." + ("wav" if output_format == "wav" else "mp3"))
                
                with open(applio_out, 'wb') as out_file:
                    out_file.write(response.read())
                
        except (URLError, HTTPError) as e:
            raise RuntimeError(f"Failed to connect to Applio server at {self.applio_server}: {e}")
        except Exception as e:
            raise RuntimeError(f"Applio processing failed: {e}")

        if normalize and applio_out.endswith(".wav"):
            try:
                peak_normalize_wav(applio_out, target_db)
            except (ValueError, OSError, RuntimeError):
                # Normalization failed, continue without it
                pass

        return applio_out

    def convert(self, **kw):
        in_path = kw["in_path"]
        output_format = kw.get("output_format","wav")
        normalize = kw.get("normalize", True)
        target_db = kw.get("target_db", -0.1)

        # If Applio is enabled, ensure separation is also enabled
        if kw.get("applio_enabled") and kw.get("applio_model"):
            kw["separate"] = True

        work_input = in_path
        separated_vocal_path = None
        if kw.get("separate"):
            work_input, _ = demucs_separate(in_path, stem=kw.get("stem","vocals"), model=kw.get("demucs_model"))
            separated_vocal_path = work_input

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

        # Process through Applio if enabled and vocal was separated
        applio_out_path = None
        if kw.get("applio_enabled") and separated_vocal_path and kw.get("applio_model"):
            applio_out_path = self._process_with_applio(separated_vocal_path, **kw)

        # Always return a tuple (rvc_output, applio_output) where applio_output may be None
        return (out_path, applio_out_path)

    def uvr(self, in_path, model=None, shifts=None, segment=None):
        """Separate all stems with Demucs and return a zip archive path."""
        out_dir = demucs_run(in_path, model=model, shifts=shifts, segment=segment)
        zip_tmp_dir = tempfile.mkdtemp()
        base = os.path.join(zip_tmp_dir, 'uvr_stems')
        archive_path = shutil.make_archive(base, 'zip', out_dir)
        if not os.path.exists(archive_path):
            raise FileNotFoundError("Failed to create UVR zip archive")
        return archive_path

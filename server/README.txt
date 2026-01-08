Pinned-Commit Local RVC + Optional UVR (Demucs/UVR5)
======================================================

- Pin any fork + commit at build (`RVC_REPO`, `RVC_COMMIT` build args).
- Optional **Demucs** or **UVR5** separation (`separate=true`, `separator=demucs|uvr`, `stem=vocals|other`).
- UVR-style `/uvr` endpoint that zips **all** stems (Demucs or UVR5) for the Max device's UVR mode.
- Peak-normalize WAV to -0.1 dBFS.

Build:
  docker compose build --build-arg RVC_REPO=<repo> --build-arg RVC_COMMIT=<hash>
Run:
  docker compose up -d

Models:
  models/<VOICE>/model.pth
  models/<VOICE>/added.index

Using weights.gg models:
  1) Download a weights.gg RVC archive.
  2) Unzip into `models/<VOICE>/` (new folder per voice).
  3) Rename the primary checkpoint to `model.pth` and, if present, rename the index file to `added.index`.
  4) Restart the container if it was already running so the server picks up the new files.

UVR5 Model:
  The default UVR5 model (2_HP-UVR.pth) is automatically downloaded during Docker build to /uvr5_weights/.
  You can override the model path using the `uvr_model_path` parameter in API requests.

API fields:
  /convert → file, rvc_model, output_format, pitch_change_all, index_rate, filter_radius,
             rms_mix_rate, pitch_detection_algorithm, separate, separator (demucs|uvr), 
             stem, demucs_model, uvr_model_path, normalize, target_db
  /uvr     → file, model (Demucs model name; defaults to DEMUCS_MODEL env), shifts (ensembles),
             segment (seconds, leave blank for Demucs default), use_uvr (true|false),
             uvr_model_path (optional, defaults to /uvr5_weights/2_HP-UVR.pth)

Separator Options:
  - separator=demucs (default): Uses Demucs for stem separation (htdemucs model by default)
  - separator=uvr: Uses UVR5 for stem separation (2_HP-UVR model by default)

CLI mapping:
  - If /rvc/infer_cli.py exists → WebUI flags
  - Else if /rvc/inference.py exists → Mangio flags

Use with Max device:
  server http://<server>:8000
  rvc_model <VOICE>
  (optional) separate 1, separator uvr, stem vocals, pitch_change_all -3

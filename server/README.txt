Pinned-Commit Local RVC + Optional UVR (Demucs)
================================================

- Pin any fork + commit at build (`RVC_REPO`, `RVC_COMMIT` build args).
- Optional **Demucs** separation (`separate=true`, `stem=vocals|drums|bass|other`).
- UVR-style `/uvr` endpoint that zips **all** stems (Demucs) for the Max device’s UVR mode.
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

API fields:
  /convert → file, rvc_model, output_format, pitch_change_all, index_rate, filter_radius,
             rms_mix_rate, pitch_detection_algorithm, separate, stem, demucs_model,
             normalize, target_db
  /uvr     → file, model (Demucs model name; defaults to DEMUCS_MODEL env), shifts (ensembles),
             segment (seconds, leave blank for Demucs default)

CLI mapping:
  - If /rvc/infer_cli.py exists → WebUI flags
  - Else if /rvc/inference.py exists → Mangio flags

Use with Max device:
  server http://<server>:8000
  rvc_model <VOICE>
  (optional) separate 1, stem vocals, pitch_change_all -3

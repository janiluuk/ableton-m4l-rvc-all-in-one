Pinned-Commit Local RVC + Optional UVR (Demucs)
================================================

- Pin any fork + commit at build (`RVC_REPO`, `RVC_COMMIT` build args).
- Optional **Demucs** separation (`separate=true`, `stem=vocals|drums|bass|other`).
- Peak-normalize WAV to -0.1 dBFS.

Build:
  docker compose build --build-arg RVC_REPO=<repo> --build-arg RVC_COMMIT=<hash>
Run:
  docker compose up -d

Models:
  models/<VOICE>/model.pth
  models/<VOICE>/added.index

API fields:
  file, rvc_model, output_format, pitch_change_all, index_rate, filter_radius,
  rms_mix_rate, pitch_detection_algorithm, separate, stem, normalize, target_db

CLI mapping:
  - If /rvc/infer_cli.py exists → WebUI flags
  - Else if /rvc/inference.py exists → Mangio flags

Use with Max device:
  server http://<server>:8000
  rvc_model <VOICE>
  (optional) separate 1, stem vocals, pitch_change_all -3

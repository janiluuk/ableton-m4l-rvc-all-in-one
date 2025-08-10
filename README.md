
Ableton Max4Live RVC All-In-One Stack
=======================================

This bundle gives you **one Max for Live device** that can switch between **Replicate (cloud)** and **Local GPU** backends, plus a **Dockerized local server** (fork/commit pinning, optional Demucs separation, peak normalization).

Folders:
- device_unified/ → The Max device (`RVC_Unified_Device.maxpat`) + unified Node script + npm deps.
- server_local_pinned_uvr/ → FastAPI + Docker server (WebUI or Mangio fork; commit pinning; Demucs option).

Quick Start — Local GPU
1) `cd server_local_pinned_uvr`
2) Build & run (WebUI latest):
   ```bash
   docker compose build      --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git      --build-arg RVC_COMMIT=
   docker compose up -d
   ```
3) Put models:
   ```
   server_local_pinned_uvr/models/<VOICE>/model.pth
   server_local_pinned_uvr/models/<VOICE>/added.index   # optional
   ```
4) In the Live device:
   - Backend: **Local**
   - Server: `http://<server>:8000`
   - `rvc_model <VOICE>`

Quick Start — Replicate
1) `cd device_unified && npm install`
2) In the device: Backend **Replicate**, paste your API token.
3) Use `rvc_model` or `model_url`, set pitch knob, drop a file, click **Process**.

Extra features
- Session/Arrangement auto-drop, New Track button.
- Takes history + re-drop.
- Clip naming + color.
- WAV normalization to −0.1 dBFS (Replicate client; Local server normalizes itself).

Notes
- You can pin a specific RVC fork/commit via Docker build args in `server_local_pinned_uvr`.
- If your fork uses different CLI flags, edit `server/rvc_infer.py` (centralized mapping).

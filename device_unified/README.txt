
RVC Unified Max for Live Device
===============================

- One device with a **Backend** toggle: **Replicate**, **Local**, or **StableAudio**.
- Front-panel **Pitch Shift (semitones)** knob.
- Session/Arrangement auto-drop, new track drop, takes history, naming & color.
- WAV normalization to −0.1 dBFS for Replicate backend.

Setup:
1) Open `RVC_Unified_Device.maxpat` in Max (or wrap as a M4L Audio Effect).
2) In the same folder, run:
   npm install
3) Choose backend:
   - Replicate: paste API token in the device (top-left).
   - Local: set `server http://YOUR_SERVER:8000` in the server field.
   - StableAudio: set `backend StableAudio`, paste your Stability API key with `stability_apikey <TOKEN>`,
     optionally point `stability_server` to a self-hosted instance, and set `stable_prompt` if your
     endpoint requires a prompt alongside the input audio.

Usage:
- Set `rvc_model` or `model_url` (Replicate) / `rvc_model` (Local; matches `/models/<name>` on server).
- Turn **Pitch Shift (st)**, drop a vocal file, click **Process** (honors the selected Mode).
- Pick destination mode: Session (highlighted), Arrangement (playhead), or New Track.
- To hit a Stable Audio–compatible local endpoint with the same dropped file, switch Mode to **Stable Audio** and
  press **Process** after setting `stability_server` and (optionally) `stable_prompt`.
- To split a clip with Ultimate Vocal Remover locally and return **all stems**, switch Mode to **UVR**, set `server` to your
  local API (default `http://127.0.0.1:8000`), and (optionally) set `uvr_model` to a Demucs model name like `htdemucs_mmi`,
  `uvr_shifts` (Demucs ensembles: higher = slower but cleaner), and `uvr_segment` (segment length in seconds; 0 = Demucs default).
- If you need a local Stable Audio endpoint, you can run one with Docker, e.g.:
  `docker run --rm -p 7860:7860 --gpus all ghcr.io/stability-ai/stable-audio-tools:latest stable-audio-api --host 0.0.0.0 --port 7860`
  then set `stability_server http://127.0.0.1:7860` in the device.

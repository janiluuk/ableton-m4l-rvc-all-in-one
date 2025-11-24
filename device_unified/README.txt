
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
- Turn **Pitch Shift (st)**, drop a vocal file, click **Process with RVC**.
- Pick destination mode: Session (highlighted), Arrangement (playhead), or New Track.

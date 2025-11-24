
Ableton Max4Live RVC All-In-One Stack
=======================================

This bundle lets you drop in a user-provided audio file and choose how to process it:

- **Ultimate Vocal Remover (UVR5)** via the bundled local API: switch the Mode menu to **UVR (all stems)** and the device will POST your file to `/uvr` on the local server, unzip every returned stem, and drop each one as its own Live track. You can forward the Demucs model name plus **UVR shifts** (ensembles for quality) and **segment length** (seconds, to control memory/speed) from the device UI so the API receives every vital separation parameter.
- **Stable Audio** mode: posts the dropped file plus your prompt to a Stable Audio–compatible API (local by default) and brings the generated audio back as a new track.

Under the hood you still have a single Max for Live device that can switch between **Replicate (cloud)** and **Local GPU** backends, plus a **Dockerized local server** (fork/commit pinning, optional Demucs separation, peak normalization).

Folders:
- device_unified/ → The Max device (`RVC_Unified_Device.maxpat`) + unified Node script + npm deps.
- server/ → FastAPI + Docker server (WebUI or Mangio fork; commit pinning; Demucs option).

Quick Start — Local GPU
1) `cd server`
2) Build & run (WebUI latest):
   ```bash
   docker compose build      --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git      --build-arg RVC_COMMIT=
   docker compose up -d
   ```
3) Put models:
   ```
   server/models/<VOICE>/model.pth
   server/models/<VOICE>/added.index   # optional
   ```
4) In the Live device:
   - Backend: **Local**
   - Server: `http://<server>:8000`
   - `rvc_model <VOICE>`

Quick Start — Replicate
1) `cd device_unified && npm install`
2) In the device: Backend **Replicate**, paste your API token.
3) Use `rvc_model` or `model_url`, set pitch knob, drop a file, click **Process**.

Processing modes with your audio file
- Drop an audio clip onto the device.
- To run **Ultimate Vocal Remover (all stems)**, set **Backend → Local**, set `server http://<server>:8000`, and pick **Mode → UVR**.
  The device POSTs your file plus `uvr_model` (Demucs name), optional `uvr_shifts` (number of ensembles), and `uvr_segment` (segment length in seconds; 0 = Demucs default) to `/uvr`, saves the returned zip of stems locally, and drops
  every stem as a new track.
- To run **Stable Audio** instead of UVR/voice conversion, switch **Mode → Stable Audio**. The device POSTs the dropped file as
  `input_audio`, your prompt (from the `stable_prompt` UI field) as `prompt`, and `output_format` to `/v2beta/stable-audio/transform`
  so the API has every required field. The returned audio is written to disk and dropped back into Live as a new track.

Extra features
- Session/Arrangement auto-drop, New Track button.
- Takes history + re-drop.
- Clip naming + color.
- WAV normalization to −0.1 dBFS (Replicate client; Local server normalizes itself).

Notes
- You can pin a specific RVC fork/commit via Docker build args in `server`.
- If your fork uses different CLI flags, edit `server/server/rvc_infer.py` (centralized mapping).

Docker — Local Stable Audio transform (optional)
------------------------------------------------
The Max device’s **Stable Audio** mode posts your dropped file to a local HTTP endpoint at
`/v2beta/stable-audio/transform`. You can stand this up with Docker:

```bash
# Uses GPU if available; caches models under ./stable-audio-cache
docker run --rm -p 7860:7860 --gpus all \
  -v $(pwd)/stable-audio-cache:/root/.cache/stabilityai \
  ghcr.io/stability-ai/stable-audio-tools:latest \
  stable-audio-api --host 0.0.0.0 --port 7860
```

Then, in the device, pick **Mode → Stable Audio**, set `stability_server http://127.0.0.1:7860`
and (optionally) a `stable_prompt`, and press **Process**.

Docker — Local RVC server + weights.gg models
---------------------------------------------
`server/` already ships with a `docker-compose.yml` that builds and runs the
FastAPI RVC server (and now exposes a UVR `/uvr` endpoint). To run it and load community models from weights.gg:

```bash
cd server
docker compose build --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git \
  --build-arg RVC_COMMIT=
docker compose up -d

# Download a weights.gg RVC archive and unpack it into models/<VOICE>/
unzip ~/Downloads/your_weightsgg_voice.zip -d models/YourVoice
mv models/YourVoice/*.pth models/YourVoice/model.pth          # ensure the filename matches
mv models/YourVoice/*.index models/YourVoice/added.index      # optional index
```

In the Max device set **Backend → Local**, `server http://127.0.0.1:8000`, and `rvc_model YourVoice`
to use that model.

Docker — UVR/Ultimate Vocal Remover API
--------------------------------------
The same `server` container also exposes `/uvr`, which runs Demucs/UVR locally and returns a zip with all stems.
Launch it with Docker and point the device to it when you select **Mode → UVR**:

```bash
cd server
docker compose build
docker compose up -d
# Optional: pick a specific Demucs model (e.g., htdemucs_mmi)
DEMUCS_MODEL=htdemucs_mmi docker compose up -d
```

By default the UVR endpoint listens on port 8000. In the device, set `server http://127.0.0.1:8000` and (optionally)
`uvr_model htdemucs_mmi`, `uvr_shifts 1` (set higher for more ensembles/quality), or `uvr_segment 6` (seconds, lower to save memory)
before pressing **Process** in UVR mode.

Docker Compose — RVC server + Stable Audio (both optional)
---------------------------------------------------------
If you want to boot **both** the local RVC server and an optional local Stable Audio endpoint in one
go (with NVIDIA GPU resources exposed to both containers), you can use the root-level
`docker-compose.example.yml` as a starting point:

```bash
cp docker-compose.example.yml docker-compose.yml
docker compose build rvc
docker compose up -d
```

This will:
- Build and run the pinned RVC FastAPI server on `http://localhost:8000` with `server/models`
  mounted for your checkpoints.
- Run `ghcr.io/stability-ai/stable-audio-tools:latest` on `http://localhost:7860` with a persisted cache under
  `./stable-audio-cache`.

Both services request `all` NVIDIA GPUs via Compose `deploy.resources.reservations.devices`. If you only want one of
the containers, comment the other service out before running `docker compose up -d`.

Quick endpoint checks
---------------------
You can verify the documented flows without Ableton/Max by calling the HTTP endpoints directly:

```bash
# Voice conversion via the local RVC server
curl -o /tmp/out.wav -F file=@/path/to/your.wav -F rvc_model=YourVoice \
  -F output_format=wav -F pitch_change_all=0 http://127.0.0.1:8000/convert

# UVR/Demucs all-stems zip (includes shifts/segment parameters exposed in the UI)
curl -o /tmp/stems.zip -F file=@/path/to/your.wav -F model=htdemucs_mmi \
  -F shifts=1 -F segment=6 http://127.0.0.1:8000/uvr

# Stable Audio transform (posts the same fields as the device: input_audio, prompt, output_format)
curl -o /tmp/stable.wav -H "Accept: audio/*" -F input_audio=@/path/to/your.wav \
  -F prompt="dark cinematic" -F output_format=wav \
  http://127.0.0.1:7860/v2beta/stable-audio/transform
```

Each command mirrors the UI wiring described above so you can confirm that the README flows are live on your stack (audio in,
audio back out, plus UVR zip extraction when expected).

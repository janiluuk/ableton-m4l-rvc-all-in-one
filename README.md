Ableton Max4Live RVC All-In-One Stack
=======================================

This project bundles a single Max for Live device that can:

- Separate stems with **Ultimate Vocal Remover (UVR5)**.
- Convert or transform audio with **Stable Audio** or **RVC voice conversion**.

You can run everything locally with Docker or use the Replicate cloud backend. The steps below focus on the simplest, “just make it work” path.

What’s in the repo
- `device_unified/` → the Max device (`RVC_Unified_Device.maxpat`), its Node script, and npm deps.
- `server_local_pinned_uvr/` → the FastAPI + Docker server for local processing.

Fast start: local GPU (recommended)
-----------------------------------
1. Install Docker with GPU support (NVIDIA drivers + Docker Engine).
2. Open a terminal and run:
   ```bash
   cd server_local_pinned_uvr
   docker compose build      --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git --build-arg RVC_COMMIT=
   docker compose up -d
   ```
3. Put your model files in `server_local_pinned_uvr/models/<VOICE>/`:
   - `model.pth`
   - `added.index` (optional)
4. In Ableton Live, drop the Max device onto a track and set:
   - Backend: **Local**
   - Server: `http://127.0.0.1:8000`
   - `rvc_model <VOICE>`
5. Drop an audio file on the device and press **Process**.

Fast start: Replicate (cloud)
-----------------------------
1. Install the Max device’s npm deps once:
   ```bash
   cd device_unified
   npm install
   ```
2. In the device UI choose **Backend → Replicate**, paste your API token, pick a model (`rvc_model` or `model_url`), drop a file, and hit **Process**.

Pick a processing mode
- **UVR (all stems)**: set **Backend → Local**, set `server http://127.0.0.1:8000`, and choose **Mode → UVR**. The device sends your file to `/uvr`, downloads a zip of stems, and drops each stem on its own track. You can pass a Demucs model name with `uvr_model`, add ensembles with `uvr_shifts`, or tweak memory use with `uvr_segment` (seconds).
- **Stable Audio**: choose **Mode → Stable Audio**. The device posts the dropped file plus your `stable_prompt` (optional) to `/v2beta/stable-audio/transform` and returns the generated audio as a new track.
- **Voice conversion (RVC)**: choose **Mode → Voice** (default). The device sends your file to the selected RVC backend using the `rvc_model` you set.

Extra quality-of-life features
- Auto-drop to Session/Arrangement, new track button, take history and re-drop, clip naming/color, and built-in WAV normalization.

Optional: local Stable Audio in one command
-------------------------------------------
If you want to run Stable Audio locally, start the official container (uses GPU if available):

```bash
  docker run --rm -p 7860:7860 --gpus all \
  -v $(pwd)/stable-audio-cache:/root/.cache/stabilityai \
  ghcr.io/stability-ai/stable-audio-tools:latest \
  stable-audio-api --host 0.0.0.0 --port 7860
```

Then set **Mode → Stable Audio** and `stability_server http://127.0.0.1:7860` in the device.

Optional: load community RVC models
-----------------------------------

**Method 1: Use the download script (recommended)**

The repository includes a download script that automatically downloads, extracts, and organizes model files:

```bash
# Download from weights.gg or any direct URL
python3 download_model.py <URL> <VoiceName>

# Example:
python3 download_model.py https://weights.gg/models/example.zip MyVoice

# Or use the shell script wrapper:
./download_model.sh https://weights.gg/models/example.zip MyVoice
```

The script will:
- Download the model file (zip or pth)
- Extract and organize files into `server/models/<VoiceName>/`
- Rename files to the expected format (`model.pth`, `added.index`)

Then start the server and use the model:

```bash
cd server
docker compose build --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git \
  --build-arg RVC_COMMIT=
docker compose up -d
```

In the device set **Backend → Local**, `server http://127.0.0.1:8000`, and `rvc_model YourVoice`.

**Method 2: Manual installation**

Alternatively, you can manually download and organize model files:

```bash
cd server
docker compose build --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git \
  --build-arg RVC_COMMIT=
docker compose up -d

unzip ~/Downloads/your_weightsgg_voice.zip -d models/YourVoice
mv models/YourVoice/*.pth models/YourVoice/model.pth
mv models/YourVoice/*.index models/YourVoice/added.index   # optional
```

In the device set **Backend → Local**, `server http://127.0.0.1:8000`, and `rvc_model YourVoice`.

Optional: UVR/Ultimate Vocal Remover endpoint
---------------------------------------------
The same local server exposes `/uvr` for Demucs/UVR separation. Launch it and point the device to it when **Mode → UVR** is selected:

```bash
cd server
docker compose build
docker compose up -d
# Optional: pick a specific Demucs model (e.g., htdemucs_mmi)
DEMUCS_MODEL=htdemucs_mmi docker compose up -d
```

Set `server http://127.0.0.1:8000` in the device. Adjust `uvr_model`, `uvr_shifts`, or `uvr_segment` before pressing **Process**.

Optional: one-compose setup for RVC + Stable Audio
--------------------------------------------------
Use the provided example to boot both local services with NVIDIA GPU access:

```bash
cp docker-compose.example.yml docker-compose.yml
docker compose build rvc
docker compose up -d
```

- RVC/UVR server runs at `http://localhost:8000` and mounts `server_local_pinned_uvr/models`.
- Stable Audio runs at `http://localhost:7860` with cache under `./stable-audio-cache`.

Comment out either service in `docker-compose.yml` if you only need one.

Ableton Max4Live RVC All-In-One Stack
=======================================

This project bundles a single Max for Live device that can:

- Separate stems with **Ultimate Vocal Remover (UVR5)**.
- Process stems with advanced effects using **StemXtract**.
- Convert or transform audio with **Stable Audio** or **RVC voice conversion**.

You can run everything locally with Docker or use the Replicate cloud backend. The steps below focus on the simplest, “just make it work” path.

## 📦 New to this plugin? Start here!

**👉 [Complete Installation Guide](INSTALLATION.md)** - Step-by-step instructions for installing the M4L device in Ableton Live, including:
- Prerequisites and requirements
- Installing the Max for Live device
- Setting up the backend (Local or Cloud)
- First-time configuration
- Troubleshooting common issues

What’s in the repo
- `device_unified/` → the Max device (`RVC_Unified_Device.maxpat`), its Node script, and npm deps.
- `server/` → the FastAPI + Docker server for local processing.

Fast start: local GPU (recommended)
-----------------------------------
1. Install Docker with GPU support (NVIDIA drivers + Docker Engine).
2. Open a terminal in the repository root and run:
   ```bash
   docker compose -f docker-compose.rvc.yml build --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git --build-arg RVC_COMMIT=
   docker compose -f docker-compose.rvc.yml up -d
   ```
3. Put your model files in `server/models/<VOICE>/`:
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
- **UVR (all stems)**: set **Backend → Local**, set `server http://127.0.0.1:8000`, and choose **Mode → UVR**. The device sends your file to `/uvr`, downloads a zip of stems, and drops each stem on its own track. Optional parameters:
  - `uvr_model` (default: `htdemucs`) - Demucs model name for stem separation
  - `uvr_shifts` (default: `1`) - Number of random shifts for improved quality (higher = slower but cleaner)
  - `uvr_segment` (default: Demucs default) - Segment length in seconds for memory management (0 uses Demucs default)
- **StemXtract (stems with effects)**: set **Mode → StemXtract**, configure your StemXtract server URL, and choose processing options. See [StemXtract Integration Guide](STEMXTRACT.md) for detailed documentation on using advanced stem separation with real-time volume, EQ, compression, reverb, and delay effects.
- **Stable Audio**: choose **Mode → Stable Audio**. The device posts the dropped file plus your `stable_prompt` (optional) to `/v2beta/stable-audio/transform` and returns the generated audio as a new track.
- **Voice conversion (RVC)**: choose **Mode → Voice** (default). The device sends your file to the selected RVC backend using the `rvc_model` you set. Add `separate true` to automatically separate vocals before conversion, enabling a chained workflow (stem separation → voice conversion).
- **Applio processing**: when using voice conversion with vocal separation enabled, you can additionally process the separated vocals through Applio by setting `applio_enabled true` and `applio_model <MODEL>`. This will generate both the standard RVC output and an additional Applio-processed output file.

Extra quality-of-life features
- Auto-drop to Session/Arrangement, new track button, take history and re-drop, clip naming/color, and built-in WAV normalization.

Optional: local Stable Audio in one command
-------------------------------------------
If you want to run Stable Audio locally, use the dedicated compose file:

```bash
docker compose -f docker-compose.stable-audio.yml up -d
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

Then start the RVC server:

```bash
docker compose -f docker-compose.rvc.yml build --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git \
  --build-arg RVC_COMMIT=
docker compose -f docker-compose.rvc.yml up -d
```

In the device set **Backend → Local**, `server http://127.0.0.1:8000`, and `rvc_model YourVoice`.

**Method 2: Manual installation**

Alternatively, you can manually download and organize model files:

```bash
# Start the RVC server first
docker compose -f docker-compose.rvc.yml build --build-arg RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git \
  --build-arg RVC_COMMIT=
docker compose -f docker-compose.rvc.yml up -d

# Then manually organize your models
unzip ~/Downloads/your_weightsgg_voice.zip -d server/models/YourVoice
mv server/models/YourVoice/*.pth server/models/YourVoice/model.pth
mv server/models/YourVoice/*.index server/models/YourVoice/added.index   # optional
```

In the device set **Backend → Local**, `server http://127.0.0.1:8000`, and `rvc_model YourVoice`.

Optional: UVR/Ultimate Vocal Remover endpoint
---------------------------------------------
The RVC server exposes `/uvr` for Demucs/UVR separation. Launch it and point the device to it when **Mode → UVR** is selected:

```bash
docker compose -f docker-compose.rvc.yml build
docker compose -f docker-compose.rvc.yml up -d
# Optional: pick a specific Demucs model (e.g., htdemucs_mmi)
DEMUCS_MODEL=htdemucs_mmi docker compose -f docker-compose.rvc.yml up -d
```

Set `server http://127.0.0.1:8000` in the device. The UVR endpoint uses these defaults:
- `uvr_model`: `htdemucs` (recommended, 4-stem separation)
- `uvr_shifts`: `1` (good balance between quality and speed)
- `uvr_segment`: Uses Demucs default (optimized for memory)

You can override any of these parameters before pressing **Process**.

Optional: Applio integration
-----------------------------
To use Applio for additional voice processing after vocal separation:

**With Docker Compose (Recommended):**

The Applio service runs in its own container and is automatically configured when you use the RVC+Applio compose file:

```bash
docker compose -f docker-compose.rvc-applio.yml build
docker compose -f docker-compose.rvc-applio.yml up -d
```

This starts both the RVC server (port 8000) and Applio service (port 8001). They share the same `/models` volume.

**Usage:**
1. Place your Applio-compatible models in `server/models/<MODEL_NAME>/` with:
   - `model.pth`
   - `added.index` (optional)
2. In the device, set `applio_enabled true` and `applio_model <MODEL_NAME>`.
3. The server will return both the standard RVC output and an additional Applio-processed output in a zip file.

**Note:** Separation is automatically enabled when Applio processing is requested.

**API Endpoints:**
- `GET http://localhost:8000/models` - List available RVC models
- `GET http://localhost:8000/applio/models` - List available Applio models (proxies to Applio service)
- `GET http://localhost:8001/models` - List models directly from Applio service
- `GET http://localhost:8001/health` - Health check for Applio service

Example API response:
```json
{
  "models": [
    {"name": "MyVoiceModel", "has_index": true},
    {"name": "AnotherModel", "has_index": false}
  ]
}
```

Optional: Pre-download UVR/Demucs models
-----------------------------------------

Demucs models are automatically downloaded on first use, but you can pre-download them for offline use or faster startup:

```bash
# List available models
python3 download_uvr_model.py --list

# Download a specific model (e.g., htdemucs)
python3 download_uvr_model.py htdemucs

# Or use the shell script wrapper
./download_uvr_model.sh htdemucs
```

Available models include:
- `htdemucs` (default, recommended) - 4-stem separation: vocals, drums, bass, other
- `htdemucs_ft` - Fine-tuned version
- `htdemucs_6s` - 6-stem separation
- `htdemucs_mmi` - Special version
- `mdx`, `mdx_extra`, `mdx_q`, `mdx_extra_q` - MDX models

Optional: run all services together (RVC + Applio + Stable Audio)
------------------------------------------------------------------
To run all services at once with NVIDIA GPU access, use the all-in-one compose file:

```bash
docker compose -f docker-compose.all.yml build
docker compose -f docker-compose.all.yml up -d
```

This starts:
- RVC/UVR server at `http://localhost:8000` (mounts `server/models`)
- Applio service at `http://localhost:8001` (shares the same models directory)
- Stable Audio at `http://localhost:7860` (cache under `./stable-audio-cache`)

**Alternative:** Copy and customize the example file:

```bash
cp docker-compose.example.yml docker-compose.yml
# Edit docker-compose.yml to comment out services you don't need
docker compose build
docker compose up -d
```

**Available compose files:**
- `docker-compose.rvc.yml` - RVC only (for voice conversion and UVR)
- `docker-compose.rvc-applio.yml` - RVC + Applio integration
- `docker-compose.stable-audio.yml` - Stable Audio only
- `docker-compose.all.yml` - All services together

**Note:** The root-level compose files use modern Docker Compose Specification syntax. The `server/docker-compose.yml` is maintained for backward compatibility and uses legacy syntax. Both work identically but the root-level files are recommended for new deployments.

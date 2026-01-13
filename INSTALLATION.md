# Max for Live Device Installation Guide

This guide walks you through installing and setting up the RVC Unified Max for Live device in Ableton Live.

## Prerequisites

Before you begin, make sure you have:

1. **Ableton Live** (version 10 or later) with **Max for Live** installed
   - Max for Live is included with Ableton Live Suite
   - For Ableton Live Standard or Intro, you need to purchase Max for Live separately
2. **Max** (optional, only needed if you want to modify the device)
   - Download from [Cycling '74](https://cycling74.com/downloads)
3. **Node.js** (version 14 or later)
   - Download from [nodejs.org](https://nodejs.org/)
4. **Git** (to clone this repository)
   - Download from [git-scm.com](https://git-scm.com/)

## Installation Steps

### Step 1: Clone the Repository

Open a terminal and clone this repository:

```bash
git clone https://github.com/janiluuk/ableton-m4l-rvc-all-in-one.git
cd ableton-m4l-rvc-all-in-one
```

### Step 2: Install Node.js Dependencies

The Max for Live device requires Node.js modules to function. Install them by running:

```bash
cd device_unified
npm install
```

This installs the required dependencies in the `device_unified` folder where the Max patch is located.

### Step 3: Create the Max for Live Device

You have two options to use the device in Ableton Live:

#### Option A: Use the .maxpat File Directly (Simplest)

1. Open Ableton Live
2. In Ableton, go to **View → Browser** to open the Browser panel
3. Navigate to **Places** in the Browser
4. Click **Add Folder** and browse to: `device_unified/RVC_Unified_Device.maxpat`
5. Drag the `RVC_Unified_Device.maxpat` file from your file browser directly onto an audio track in Ableton
6. The device will load as a Max Audio Effect

**Note**: This method loads the uncompiled patch. It's easier but may have slightly slower load times.

#### Option B: Freeze as .amxd Device (Recommended for Distribution)

If you want to create a standalone frozen device:

1. Open **Max** (standalone application)
2. In Max, go to **File → Open** and select `device_unified/RVC_Unified_Device.maxpat`
3. Once the patch is open, go to **File → Freeze Device** (or press the ❄️ Freeze button in the device toolbar)
4. Save the frozen device as `RVC_Unified_Device.amxd` in a location you can remember:
   - Recommended: Save directly to your Ableton User Library (see paths in Step 4 below)
   - This makes it immediately available in your Ableton Browser under **User Library → Audio Effects → Max Audio Effect**
   - Alternatively, save anywhere and copy it to the User Library later
5. The device is now frozen and ready to use in Ableton Live

### Step 4: Add the Device to Your Ableton User Library (Optional)

To make the device easily accessible in Ableton's Browser:

1. In your file browser, copy the `RVC_Unified_Device.amxd` file (or the entire `device_unified` folder)
2. Paste it into your Ableton User Library location:
   - **macOS**: `~/Music/Ableton/User Library/Presets/Audio Effects/Max Audio Effect/`
   - **Windows**: `\Users\[username]\Documents\Ableton\User Library\Presets\Audio Effects\Max Audio Effect\`
3. Restart Ableton Live
4. The device will now appear in your Browser under **User Library → Audio Effects → Max Audio Effect**

## Setting Up the Backend

The Max for Live device needs a backend server to process audio. You have two options:

### Option 1: Local Backend (Recommended for Best Quality)

Run your own processing server using Docker. This requires:
- Docker with GPU support (NVIDIA GPU + drivers)
- At least 8GB GPU VRAM recommended

**Quick Setup:**

1. **Start the RVC server:**
   ```bash
   cd /path/to/ableton-m4l-rvc-all-in-one
   docker compose -f docker-compose.rvc.yml build
   docker compose -f docker-compose.rvc.yml up -d
   ```
   
   Note: The build command automatically uses the default RVC repository. To pin to a specific commit, add `--build-arg RVC_COMMIT=<commit-hash>`.

2. **Add voice models:**
   Place your RVC model files in `server/models/<VoiceName>/`:
   - `model.pth` (required)
   - `added.index` (optional, improves quality)

   You can use the download script to automatically download models:
   ```bash
   python3 download_model.py <URL> <VoiceName>
   ```

3. **Verify the server is running:**
   ```bash
   curl http://localhost:8000/models
   ```

### Option 2: Replicate Backend (Cloud-Based, Easiest)

Use Replicate's cloud API for processing:

1. Sign up at [replicate.com](https://replicate.com/)
2. Get your API token from your account settings
3. You'll paste this token in the device UI (see Usage section below)

**Note**: The Replicate backend may incur costs based on usage and has quality limitations compared to local processing.

## First-Time Setup in Ableton Live

Once you have the device installed:

1. **Add the device to a track:**
   - Drag `RVC_Unified_Device` from the Browser onto an audio track
   - Or drag the `.maxpat` or `.amxd` file directly onto a track

2. **Configure the backend:**

   **For Local Backend:**
   - Set **Backend** to `Local`
   - In the device, type: `server http://127.0.0.1:8000`
   - Type: `rvc_model <VoiceName>` (match the folder name in `server/models/`)

   **For Replicate Backend:**
   - Set **Backend** to `Replicate`
   - Paste your Replicate API token in the API key field
   - Type: `model_url <ReplicateModelURL>` or use the default

3. **Set processing mode:**
   - **Voice** (default): Voice conversion using RVC
   - **UVR**: Stem separation (splits audio into vocals, drums, bass, other)
   - **Stable Audio**: AI audio transformation

## Usage Quick Start

### Basic Voice Conversion

1. Configure backend and model (see First-Time Setup above)
2. Adjust **Pitch Shift** knob if needed (semitones)
3. Drag an audio file onto the device's drop zone
4. Click **Process**
5. Wait for processing to complete
6. The processed audio will be automatically added to your Ableton session

### Stem Separation (UVR Mode)

1. Set **Mode** to `UVR`
2. Set **Backend** to `Local` with server URL: `http://127.0.0.1:8000`
3. (Optional) Set parameters:
   - `uvr_model htdemucs` (or other Demucs models)
   - `uvr_shifts 1` (higher = better quality but slower)
4. Drag an audio file onto the drop zone
5. Click **Process**
6. Each stem (vocals, drums, bass, other) will be added as a separate track

## Troubleshooting

### "Missing module" or "node.script: error loading script" errors

This means Node.js dependencies weren't installed properly:

1. Open Terminal/Command Prompt
2. Navigate to the device folder:
   ```bash
   cd /path/to/ableton-m4l-rvc-all-in-one/device_unified
   ```
3. Delete the `node_modules` folder if it exists:
   ```bash
   rm -rf node_modules  # macOS/Linux
   rmdir /s /q node_modules  # Windows
   ```
4. Reinstall dependencies:
   ```bash
   npm install
   ```
5. If you froze the device, you need to re-freeze it after reinstalling dependencies

### Device doesn't appear in Ableton Browser

- Make sure you placed the `.amxd` file in the correct User Library location
- Restart Ableton Live completely
- Check that Max for Live is properly installed and licensed

### "Server connection failed" error

**For Local Backend:**
- Verify Docker container is running: `docker ps`
- Check server logs: `docker compose -f docker-compose.rvc.yml logs`
- Test the server manually: `curl http://localhost:8000/models`
- Make sure port 8000 isn't blocked by firewall

**For Replicate Backend:**
- Verify your API token is correct
- Check your internet connection
- Check Replicate service status

### Processing takes forever or fails

**For Local Backend:**
- Check GPU availability: `nvidia-smi` (NVIDIA GPUs)
- Monitor Docker logs for errors
- Ensure you have enough GPU VRAM (8GB+ recommended)
- Try a smaller audio file first

**For Replicate Backend:**
- Check file size (Replicate has limits)
- Verify your Replicate account has credits
- Try again later (cloud services may have temporary issues)

### Audio quality is poor

- For voice conversion, make sure you're using a high-quality RVC model
- Enable `separate` mode to isolate vocals before processing
- Adjust pitch shift carefully (large shifts degrade quality)
- For local backend, ensure you have the `.index` file for better quality
- Try different values for `index_rate` (0.0-1.0, default 0.75)

### Device freezes Ableton

- This usually happens during long processing operations
- The device processes asynchronously, but very large files can still cause issues
- Try processing shorter audio clips (under 1 minute for testing)
- Check the device's status message for progress

## Next Steps

- See the main [README.md](README.md) for detailed information about all processing modes and parameters
- Check [FREEZE_ME_FIRST.txt](FREEZE_ME_FIRST.txt) for quick reference on freezing the device
- Explore advanced features like Applio integration and custom model management

## Need Help?

If you encounter issues not covered here:
1. Check the [GitHub Issues](https://github.com/janiluuk/ableton-m4l-rvc-all-in-one/issues) page
2. Review the server logs: `docker compose -f docker-compose.rvc.yml logs`
3. Open a new issue with details about your setup and the error you're seeing

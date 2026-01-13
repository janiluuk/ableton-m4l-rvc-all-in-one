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
   - Recommended: Save directly to your Ableton User Library (see paths in the next section below)
   - This makes it immediately available in your Ableton Browser under **User Library → Audio Effects → Max Audio Effect**
   - Alternatively, save anywhere and copy it to the User Library later
5. The device is now frozen and ready to use in Ableton Live

### Step 4: Add the Device to Your Ableton User Library (Optional)

To make the device easily accessible in Ableton's Browser:

1. In your file browser, copy the frozen `RVC_Unified_Device.amxd` file (if you used Option B above)
   - If you used Option A (.maxpat directly), you can skip this step as the device will load from its original location
2. Paste it into your Ableton User Library location:
   - **macOS**: `~/Music/Ableton/User Library/Presets/Audio Effects/Max Audio Effect/`
   - **Windows**: `C:\Users\[username]\Documents\Ableton\User Library\Presets\Audio Effects\Max Audio Effect\`
3. Restart Ableton Live
4. The device will now appear in your Browser under **User Library → Audio Effects → Max Audio Effect**

## Setting Up the Backend

The Max for Live device needs a backend server to process audio. You have two options:

### Option 1: Local Backend (Recommended for Best Quality)

Run your own processing server using Docker. This requires:
- Docker with GPU support (NVIDIA GPU + drivers)
- At least 8GB GPU VRAM recommended

**Quick Setup:**

Note: In the commands below, replace `/path/to/ableton-m4l-rvc-all-in-one` with the actual path where you cloned the repository. Examples:
- macOS/Linux: `~/Projects/ableton-m4l-rvc-all-in-one`
- Windows: `C:\Projects\ableton-m4l-rvc-all-in-one` (or use forward slashes: `C:/Projects/ableton-m4l-rvc-all-in-one`)

1. **Start the RVC server:**
   ```bash
   cd /path/to/ableton-m4l-rvc-all-in-one
   docker compose -f docker-compose.rvc.yml build
   docker compose -f docker-compose.rvc.yml up -d
   ```
   
   **Optional:** To pin to a specific RVC commit instead of using the latest:
   ```bash
   docker compose -f docker-compose.rvc.yml build --build-arg RVC_COMMIT=abc123
   ```

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

### Chaining Processes: Stem Separation + Voice Conversion

You can chain processes together to first separate stems, then convert the voice. There are two approaches:

#### Method 1: Automatic Separation with Voice Conversion

Use the built-in `separate` parameter to automatically separate vocals before voice conversion:

1. Set **Mode** to `Voice` (default)
2. Configure your backend and RVC model as usual
3. Enable separation by typing: `separate true`
4. (Optional) Choose separator: `separator demucs` or `separator uvr` (demucs is default)
5. Drag your audio file onto the drop zone
6. Click **Process**
7. The device will:
   - First separate vocals from the mix
   - Then apply voice conversion to the isolated vocals
   - Return the converted vocal track

**Example configuration:**
```
server http://127.0.0.1:8000
rvc_model MyVoiceModel
separate true
separator demucs
```

#### Method 2: Manual Two-Step Process

For more control, manually separate first, then convert:

1. **Step 1 - Separate stems:**
   - Set **Mode** to `UVR`
   - Process your audio file
   - Wait for all stems to be added as separate tracks

2. **Step 2 - Convert the vocal stem:**
   - Set **Mode** back to `Voice`
   - Configure your RVC model: `rvc_model MyVoiceModel`
   - Drag the **vocals** track/clip onto the device
   - Click **Process**
   - The converted vocals will be added as a new track

**Tip:** The manual method gives you the opportunity to:
- Edit or clean up the separated vocals before conversion
- Try different RVC models on the same vocal stem
- Keep all intermediate stems for further processing

#### Advanced: Applio Processing Chain

You can also chain Applio processing after voice conversion with automatic separation:

```
server http://127.0.0.1:8000
rvc_model MyVoiceModel
separate true
applio_enabled true
applio_model MyApplioModel
```

This will:
1. Separate vocals from the mix
2. Apply RVC voice conversion
3. Also process through Applio for comparison
4. Return both RVC and Applio outputs

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
   # macOS/Linux
   rm -rf node_modules
   
   # Windows (PowerShell or Command Prompt)
   if exist node_modules rmdir /S /Q node_modules
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

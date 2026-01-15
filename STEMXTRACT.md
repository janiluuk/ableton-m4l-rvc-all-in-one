# StemXtract API Integration

This document describes how to use the StemXtract API integration in the Max4Live RVC device.

## Overview

The StemXtract API integration adds support for advanced stem separation with real-time effects processing using the [StemXtract Gradio API](https://github.com/TheAwakeOne/StemXtract). This allows you to:

- Separate audio into stems (vocals, drums, bass, other) with multiple AI models
- Apply volume, EQ, compression, reverb, and delay effects to individual stems
- Process and blend tracks with advanced controls
- Export final outputs and individual stems

## Prerequisites

1. A running StemXtract Gradio server (default: `http://192.168.2.12:60000`)
2. The Max4Live device installed with the updated JavaScript and server code
3. Python dependencies installed (see `server/requirements.txt`)

## Configuration

### Server Setup

The local FastAPI server acts as a proxy to the StemXtract API. To start the server:

```bash
cd server
pip install -r requirements.txt
python main.py
```

The server will start on `http://127.0.0.1:8000` by default.

### Max4Live Device Configuration

In the Max4Live device, set the following parameters:

1. **Mode**: Set to `stemxtract` or any value containing "stem"
2. **Backend**: Set to `Local`
3. **Server**: Set to your FastAPI server URL (e.g., `http://127.0.0.1:8000`)
4. **StemXtract Server**: Set to your StemXtract Gradio server URL (e.g., `http://192.168.2.12:60000`)

## Parameters

### Basic Parameters

- **stemxtract_task**: Task type
  - `remove_vocals`: Remove vocals from the track
  - `isolate_vocals`: Extract only vocals
  - `mix_stems`: Process all stems with effects
  
- **stemxtract_model**: AI model for stem separation
  - `htdemucs` (default): High-quality 4-stem separation
  - `mdx`: MDX model
  - `mdx_extra`: MDX with extra quality
  - `mdx_q`: MDX quantized (faster)

### Volume Controls

- **stemxtract_drums_vol**: Drums volume (0.0 to 2.0, default: 1.0)
- **stemxtract_bass_vol**: Bass volume (0.0 to 2.0, default: 1.0)
- **stemxtract_other_vol**: Other instruments volume (0.0 to 2.0, default: 1.0)
- **stemxtract_vocals_vol**: Vocals volume (0.0 to 2.0, default: 1.0)

### Instrumental Effects

- **stemxtract_instrumental_volume**: Overall instrumental volume (0.0 to 2.0, default: 1.0)
- **stemxtract_instrumental_low_gain**: Low frequency gain in dB (-12 to +12, default: 0.0)
- **stemxtract_instrumental_high_gain**: High frequency gain in dB (-12 to +12, default: 0.0)
- **stemxtract_instrumental_reverb**: Reverb amount (0.0 to 1.0, default: 0.0)

### Vocal Effects

- **stemxtract_vocal_volume**: Vocal volume (0.0 to 2.0, default: 1.0)
- **stemxtract_vocal_low_gain**: Vocal low frequency gain in dB (-12 to +12, default: 0.0)
- **stemxtract_vocal_high_gain**: Vocal high frequency gain in dB (-12 to +12, default: 0.0)
- **stemxtract_vocal_reverb**: Vocal reverb amount (0.0 to 1.0, default: 0.0)

### Other Options

- **stemxtract_trim_silence**: Trim silence from outputs (boolean, default: false)

## Usage Examples

### Example 1: Basic Vocal Removal

```javascript
// In Max4Live device
mode stemxtract
backend Local
server http://127.0.0.1:8000
stemxtract_server http://192.168.2.12:60000
stemxtract_task remove_vocals
stemxtract_model htdemucs
source /path/to/audio.wav
process
```

### Example 2: Vocal Isolation with Effects

```javascript
mode stemxtract
stemxtract_task isolate_vocals
stemxtract_vocal_volume 1.2
stemxtract_vocal_reverb 0.3
stemxtract_vocal_low_gain 2.0
stemxtract_trim_silence 1
source /path/to/audio.wav
process
```

### Example 3: Custom Mix with Volume Controls

```javascript
mode stemxtract
stemxtract_task mix_stems
stemxtract_drums_vol 0.8
stemxtract_bass_vol 1.2
stemxtract_other_vol 0.9
stemxtract_vocals_vol 1.5
stemxtract_instrumental_reverb 0.2
stemxtract_vocal_reverb 0.4
source /path/to/audio.wav
process
```

## API Endpoint

The FastAPI server exposes the following endpoint:

### POST `/stemxtract/process`

Processes an audio file with StemXtract API.

**Request Parameters:**
- `file` (required): Audio file to process
- `stemxtract_server`: StemXtract server URL (default: `http://192.168.2.12:60000`)
- `task`: Task type (default: `remove_vocals`)
- `model_name`: AI model (default: `htdemucs`)
- All volume and effect parameters (see Parameters section)

**Response:**
- ZIP file containing:
  - `final_output.wav`: Mixed output
  - `drums.wav`: Drums stem
  - `bass.wav`: Bass stem
  - `other.wav`: Other instruments stem
  - `vocals.wav`: Vocals stem

**Response Headers:**
- `X-Processing-Time`: Processing time in seconds

## Direct API Usage

You can also call the StemXtract API directly using Python:

```python
from stemxtract_client import StemXtractClient

# Initialize client
client = StemXtractClient(server_url="http://192.168.2.12:60000")

# Process track
result = client.process_track(
    audio_file_path="/path/to/audio.wav",
    task="remove_vocals",
    model_name="htdemucs",
    vocals_vol=1.5,
    instrumental_reverb=0.3,
    vocal_reverb=0.5
)

# Result is a tuple: (final_output, time, drums, bass, other, vocals)
final_output, processing_time, drums, bass, other, vocals = result
print(f"Processed in {processing_time}")
```

## Troubleshooting

### Server Connection Issues

If you can't connect to the StemXtract server:

1. Verify the StemXtract Gradio server is running
2. Check the server URL is correct
3. Ensure network connectivity between the Max4Live device and the server
4. Check firewall settings

### Processing Errors

If processing fails:

1. Check the audio file format (MP3, WAV, FLAC, AAC supported)
2. Verify the file size is under 50MB
3. Check server logs for detailed error messages
4. Try with a different AI model

### Performance Issues

For better performance:

1. Use `htdemucs` model for balanced quality/speed
2. Reduce the number of active effects
3. Process shorter audio clips
4. Ensure the StemXtract server has adequate CPU/GPU resources

## Integration with Existing Features

The StemXtract integration works alongside existing features:

- **UVR Mode**: Use for basic stem separation without effects
- **Voice Mode**: Use for voice conversion after stem separation
- **Stable Audio Mode**: Use for AI-based audio transformation

You can chain these modes by:
1. Processing with StemXtract to separate and apply effects
2. Using the output stems in Voice mode for conversion
3. Final polish with normalization

## References

- [StemXtract GitHub Repository](https://github.com/TheAwakeOne/StemXtract)
- [Demucs Documentation](https://github.com/facebookresearch/demucs)
- [Max4Live Device Documentation](../README.md)

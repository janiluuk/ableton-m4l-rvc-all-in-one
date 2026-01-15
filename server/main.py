# server/main.py
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import tempfile, os, shutil
import urllib.request
import json
from rvc_infer import RVCConverter
from stemxtract_client import StemXtractClient

app = FastAPI(title="RVC Local Service (Pinned + UVR)", version="0.3.0")
converter = RVCConverter()

@app.post("/convert")
async def convert_audio(
    file: UploadFile = File(...),
    rvc_model: Optional[str] = Form(None),
    output_format: Optional[str] = Form("wav"),
    # RVC params
    pitch_change_all: Optional[float] = Form(0.0),
    index_rate: Optional[float] = Form(0.5),
    filter_radius: Optional[int] = Form(3),
    rms_mix_rate: Optional[float] = Form(0.25),
    pitch_detection_algorithm: Optional[str] = Form("rmvpe"),  # or 'crepe'
    # Pre-process separation
    separate: Optional[bool] = Form(False),
    separator: Optional[str] = Form("demucs"),  # 'demucs' or 'uvr'
    stem: Optional[str] = Form("vocals"),  # 'vocals' or 'other'
    demucs_model: Optional[str] = Form(None),
    # Applio processing
    applio_enabled: Optional[bool] = Form(False),
    applio_model: Optional[str] = Form(None),
    uvr_model_path: Optional[str] = Form(None),
    # Post-process
    normalize: Optional[bool] = Form(True),
    target_db: Optional[float] = Form(-0.1)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1] or ".wav") as tmp_in:
            data = await file.read()
            tmp_in.write(data)
            in_path = tmp_in.name

        result = converter.convert(
            in_path=in_path,
            rvc_model=rvc_model,
            output_format=output_format,
            pitch_change_all=pitch_change_all,
            index_rate=index_rate,
            filter_radius=filter_radius,
            rms_mix_rate=rms_mix_rate,
            pitch_detection_algorithm=pitch_detection_algorithm,
            separate=separate,
            separator=separator,
            stem=stem,
            demucs_model=demucs_model,
            applio_enabled=applio_enabled,
            applio_model=applio_model,
            uvr_model_path=uvr_model_path,
            normalize=normalize,
            target_db=target_db
        )
        
        # Result is always a tuple (rvc_output, applio_output)
        out_path, applio_out_path = result
            
        # If Applio output exists, create a zip with both files
        if applio_out_path:
            zip_dir = tempfile.mkdtemp()
            # Copy files with descriptive names
            rvc_dest = os.path.join(zip_dir, f"rvc_output.{output_format}")
            applio_dest = os.path.join(zip_dir, f"applio_output.{output_format}")
            shutil.copy2(out_path, rvc_dest)
            shutil.copy2(applio_out_path, applio_dest)
            
            # Create zip using a secure temporary file
            zip_tmp_dir = tempfile.mkdtemp()
            base = os.path.join(zip_tmp_dir, 'rvc_applio_outputs')
            zip_path = shutil.make_archive(base, 'zip', zip_dir)
            return FileResponse(zip_path, filename="rvc_applio_outputs.zip", media_type="application/zip")
        
        return FileResponse(out_path, filename=os.path.basename(out_path), media_type="audio/wav" if out_path.endswith(".wav") else "audio/mpeg")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/uvr")
async def uvr_audio(
    file: UploadFile = File(...),
    model: Optional[str] = Form(None),
    shifts: Optional[int] = Form(None),
    segment: Optional[float] = Form(None),
    use_uvr: Optional[bool] = Form(False),
    uvr_model_path: Optional[str] = Form(None)
):
    """Expose a Demucs/UVR-style separation endpoint that returns all stems as a zip.
    
    Defaults:
        model: 'htdemucs' - Default Demucs model (4-stem separation)
        shifts: 1 - Number of random shifts for equivariant stabilization
        segment: None - Segment size in seconds (uses Demucs default if not specified)
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1] or ".wav") as tmp_in:
            data = await file.read()
            tmp_in.write(data)
            in_path = tmp_in.name

        # Apply sensible defaults
        model = model or 'htdemucs'
        shifts = shifts if shifts is not None else 1
        # segment remains None (Demucs default) if not provided or 0/0.0
        if segment is not None and segment == 0:
            segment = None

        zip_path = converter.uvr(
            in_path=in_path,
            model=model,
            shifts=shifts,
            segment=segment,
            use_uvr=use_uvr,
            uvr_model_path=uvr_model_path
        )
        return FileResponse(zip_path, filename=os.path.basename(zip_path), media_type="application/zip")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/models")
async def list_models():
    """List available RVC models in the /models directory."""
    try:
        models_dir = "/models"
        if not os.path.exists(models_dir):
            return JSONResponse({"models": []})
        
        models = []
        for item in os.listdir(models_dir):
            item_path = os.path.join(models_dir, item)
            if os.path.isdir(item_path):
                # Check if directory contains model.pth file
                model_pth = os.path.join(item_path, "model.pth")
                if os.path.exists(model_pth):
                    model_info = {
                        "name": item,
                        "has_index": os.path.exists(os.path.join(item_path, "added.index"))
                    }
                    models.append(model_info)
        
        return JSONResponse({"models": models})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/applio/models")
async def list_applio_models():
    """
    List available Applio models by querying the Applio service.
    This endpoint proxies the request to the Applio container.
    """
    try:
        applio_server = os.environ.get("APPLIO_SERVER", "http://applio:8001")
        req = urllib.request.Request(f"{applio_server}/models")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return JSONResponse(data)
    except Exception as e:
        return JSONResponse({"error": f"Failed to fetch Applio models: {str(e)}"}, status_code=500)

@app.post("/stemxtract/process")
async def stemxtract_process(
    file: UploadFile = File(...),
    stemxtract_server: Optional[str] = Form("http://192.168.2.12:60000"),
    task: Optional[str] = Form("remove_vocals"),
    model_name: Optional[str] = Form("htdemucs"),
    drums_vol: Optional[float] = Form(1.0),
    bass_vol: Optional[float] = Form(1.0),
    other_vol: Optional[float] = Form(1.0),
    vocals_vol: Optional[float] = Form(1.0),
    instrumental_volume: Optional[float] = Form(1.0),
    instrumental_low_gain: Optional[float] = Form(0.0),
    instrumental_high_gain: Optional[float] = Form(0.0),
    instrumental_reverb: Optional[float] = Form(0.0),
    vocal_volume: Optional[float] = Form(1.0),
    vocal_low_gain: Optional[float] = Form(0.0),
    vocal_high_gain: Optional[float] = Form(0.0),
    vocal_reverb: Optional[float] = Form(0.0),
    trim_silence_chk: Optional[bool] = Form(False)
):
    """
    Process audio track with StemXtract API for stem separation with effects.
    
    Returns a zip file containing the final output and individual stems.
    """
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1] or ".wav") as tmp_in:
            data = await file.read()
            tmp_in.write(data)
            in_path = tmp_in.name

        # Initialize StemXtract client
        client = StemXtractClient(server_url=stemxtract_server)
        
        # Process track
        result = client.process_track(
            audio_file_path=in_path,
            task=task,
            model_name=model_name,
            drums_vol=drums_vol,
            bass_vol=bass_vol,
            other_vol=other_vol,
            vocals_vol=vocals_vol,
            instrumental_volume=instrumental_volume,
            instrumental_low_gain=instrumental_low_gain,
            instrumental_high_gain=instrumental_high_gain,
            instrumental_reverb=instrumental_reverb,
            vocal_volume=vocal_volume,
            vocal_low_gain=vocal_low_gain,
            vocal_high_gain=vocal_high_gain,
            vocal_reverb=vocal_reverb,
            trim_silence_chk=trim_silence_chk
        )
        
        # Result is a tuple: (final_output, processing_time, drums, bass, other, vocals)
        final_output_path, processing_time, drums_path, bass_path, other_path, vocals_path = result
        
        # Create a zip file with all outputs
        zip_dir = tempfile.mkdtemp()
        output_files = {
            'final_output.wav': final_output_path,
            'drums.wav': drums_path,
            'bass.wav': bass_path,
            'other.wav': other_path,
            'vocals.wav': vocals_path
        }
        
        # Copy files to zip directory, skipping None values
        for name, src_path in output_files.items():
            if src_path and os.path.exists(src_path):
                dest = os.path.join(zip_dir, name)
                shutil.copy2(src_path, dest)
        
        # Create zip file
        zip_tmp_dir = tempfile.mkdtemp()
        base = os.path.join(zip_tmp_dir, 'stemxtract_outputs')
        zip_path = shutil.make_archive(base, 'zip', zip_dir)
        
        # Clean up input file
        os.remove(in_path)
        
        return FileResponse(
            zip_path, 
            filename="stemxtract_outputs.zip", 
            media_type="application/zip",
            headers={"X-Processing-Time": str(processing_time)}
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

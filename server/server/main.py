# server/main.py
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import tempfile, os, shutil
from rvc_infer import RVCConverter

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
    """Expose a Demucs/UVR-style separation endpoint that returns all stems as a zip."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1] or ".wav") as tmp_in:
            data = await file.read()
            tmp_in.write(data)
            in_path = tmp_in.name

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
        import urllib.request
        import json
        
        applio_server = os.environ.get("APPLIO_SERVER", "http://applio:8001")
        req = urllib.request.Request(f"{applio_server}/models")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return JSONResponse(data)
    except Exception as e:
        return JSONResponse({"error": f"Failed to fetch Applio models: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

# server/main.py
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import tempfile, os
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

        out_path = converter.convert(
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
            uvr_model_path=uvr_model_path,
            normalize=normalize,
            target_db=target_db
        )
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

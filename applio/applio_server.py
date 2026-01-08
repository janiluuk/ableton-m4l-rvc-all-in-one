#!/usr/bin/env python3
"""
Applio API Server
Provides a REST API for voice conversion using Applio.
"""
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import tempfile
import os
import subprocess

app = FastAPI(title="Applio Voice Conversion Service", version="1.0.0")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "applio"}

@app.get("/models")
async def list_models():
    """List available Applio models in the /models directory."""
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

@app.post("/convert")
async def convert_audio(
    file: UploadFile = File(...),
    model_name: Optional[str] = Form(None),
    pitch: Optional[int] = Form(0),
    index_rate: Optional[float] = Form(0.5),
    filter_radius: Optional[int] = Form(3),
    rms_mix_rate: Optional[float] = Form(0.25),
    f0_method: Optional[str] = Form("rmvpe"),
    output_format: Optional[str] = Form("wav")
):
    """
    Convert audio using Applio voice conversion.
    
    Args:
        file: Audio file to convert
        model_name: Name of the voice model to use
        pitch: Pitch shift in semitones
        index_rate: Index rate for retrieval
        filter_radius: Filter radius
        rms_mix_rate: RMS mix rate
        f0_method: F0 extraction method (rmvpe, crepe, etc.)
        output_format: Output format (wav or mp3)
    """
    try:
        # Sanitize filename - use fixed extension based on content
        file_ext = ".wav" if file.content_type and "audio" in file.content_type else ".wav"
        
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_in:
            data = await file.read()
            tmp_in.write(data)
            in_path = tmp_in.name

        # Prepare output path
        tmp_dir = tempfile.mkdtemp()
        out_path = os.path.join(tmp_dir, f"applio_out.{output_format}")

        # Build Applio command with timeout
        cmd = ["python3", "/applio/core.py", "infer",
               "--input_path", in_path,
               "--output_path", out_path]

        # Add model if specified
        if model_name:
            model_dir = os.path.join("/models", model_name)
            model_path = os.path.join(model_dir, "model.pth")
            index_path = os.path.join(model_dir, "added.index")
            
            if os.path.exists(model_path):
                cmd += ["--pth_path", model_path]
            if os.path.exists(index_path):
                cmd += ["--index_path", index_path]

        # Add parameters
        if pitch is not None:
            cmd += ["--pitch", str(pitch)]
        if index_rate is not None:
            cmd += ["--index_rate", str(index_rate)]
        if filter_radius is not None:
            cmd += ["--filter_radius", str(filter_radius)]
        if rms_mix_rate is not None:
            cmd += ["--rms_mix_rate", str(rms_mix_rate)]
        if f0_method:
            cmd += ["--f0_method", str(f0_method)]

        # Run Applio with timeout
        timeout = int(os.environ.get("APPLIO_PROCESS_TIMEOUT", "300"))  # 5 minutes default
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                            text=True, timeout=timeout)
        
        if proc.returncode != 0 or not os.path.exists(out_path):
            return JSONResponse(
                {"error": f"Applio conversion failed: {proc.stderr or proc.stdout}"},
                status_code=500
            )

        # Return the converted audio
        media_type = "audio/wav" if output_format == "wav" else "audio/mpeg"
        return FileResponse(out_path, filename=os.path.basename(out_path), media_type=media_type)
        
    except subprocess.TimeoutExpired:
        return JSONResponse({"error": "Applio processing timeout"}, status_code=504)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("applio_server:app", host="0.0.0.0", port=8001)

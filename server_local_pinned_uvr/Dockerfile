# CUDA base image
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip git ffmpeg && rm -rf /var/lib/apt/lists/*

# ---- Selectable RVC fork + commit (build args) ----
ARG RVC_REPO=https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git
ARG RVC_COMMIT=
RUN git clone ${RVC_REPO} /rvc &&     if [ -n "${RVC_COMMIT}" ]; then cd /rvc && git checkout ${RVC_COMMIT}; fi

# ---- Python deps ----
WORKDIR /app
COPY server /app
RUN pip3 install --no-cache-dir -r requirements.txt
RUN if [ -f /rvc/requirements.txt ]; then pip3 install --no-cache-dir -r /rvc/requirements.txt || true; fi

# Demucs (for UVR-style separation)
RUN pip3 install --no-cache-dir demucs==4.0.1

VOLUME ["/models", "/rvc"]
EXPOSE 8000
CMD ["python3", "main.py"]

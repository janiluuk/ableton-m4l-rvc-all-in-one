# Applio Docker container
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 python3-pip git ffmpeg && rm -rf /var/lib/apt/lists/*

# Clone Applio repository
ARG APPLIO_REPO=https://github.com/IAHispano/Applio.git
ARG APPLIO_COMMIT=
RUN git clone ${APPLIO_REPO} /applio && \
    if [ -n "${APPLIO_COMMIT}" ]; then cd /applio && git checkout ${APPLIO_COMMIT}; fi

# Install Applio dependencies
WORKDIR /applio
RUN pip3 install --no-cache-dir -r requirements.txt || true

# Copy the Applio API server
COPY applio_server.py /app/applio_server.py

WORKDIR /app
VOLUME ["/models"]
EXPOSE 8001
CMD ["python3", "applio_server.py"]

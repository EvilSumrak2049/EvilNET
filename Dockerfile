# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


# Update and fix broken packages
RUN apt-get update && apt-get install -y --fix-broken

# Install your packages, specifying versions if necessary
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libopencv-dev

RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

RUN git clone https://github.com/EvilSumrak2049/EvilNET.git .

RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu121

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "design.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.maxUploadSize=100000"]

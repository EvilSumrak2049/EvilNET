# EvilNET flying objects detector
This is streamlit project with functionality to monitor areas close to airports.

## Supported classes:
- copter
- plane
- helicopter
- bird
- drone (plane-type)

## Used technologies
- Streamlit
- YOLO
- Docker
- SQLite

## Project requirements
- Nvidia GPU + CUDA
- Python >=3.9
- Windows 10/11 / Linux / Docker

## Functionality
- Setting up video streaming devices (cameras)
- Single image detection
- Video detection
- Multiple images detection (return .zip with .txt)
- Configurable confidence threshold and image size
- Download / delete video in database-like view

## Installation
### via Docker
Prerequisites:
- Linux / WSL host system
- GPU + drivers
- Allow docker containers to use host system's GPUs

```bash
git clone https://github.com/EvilSumrak2049/EvilNET.git
cd EvilNET
docker build -t streamlit .
docker run -p 127.0.0.1:5443:8501 --gpus all streamlit
```

### manually (Windows / Linux)
Follow these instructions:
```bash
git clone https://github.com/EvilSumrak2049/EvilNET.git
cd EvilNET
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
streamlit run design.py --server.maxUploadSize=100000
```

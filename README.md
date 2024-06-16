sudo docker build -t streamlit .
sudo docker run -p 127.0.0.1:5443:8501 --gpus all streamlit
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

RUN apt-get update -y \
&& apt-get install gcc g++ git git-lfs unixodbc unixodbc-dev libodbc2 sqlite3 --no-install-recommends -y
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install -r requirements.txt
RUN pip install mlflow

RUN rm -rf /var/cache/apk/* \
    && apt-get remove gcc -y \
    && apt-get remove g++ -y \
    && apt-get remove python-dev -y \
    && apt-get remove musl-dev -y \
    && rm -rf /var/lib/apt/lists/*

RUN python -m nltk.downloader stopwords punkt
RUN pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


RUN python -c "from sentence_transformers import SentenceTransformer;\
            SentenceTransformer('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True, truncate_dim=256, device='cpu')"

WORKDIR /chat_backend
COPY . /chat_backend
# RUN git clone https://huggingface.co/nomic-ai/nomic-embed-text-v1.5 /chat_backend/nomic/nomic-embed-text-v1.5
# RUN celery -A job_handler.app worker --loglevel=info &

# USER appuser
EXPOSE 5000

# Command to run the application with gunicorn
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "--log-config", "log_config.conf", "socket_server:app"]
# CMD ["python", "socket_server.py"]
# RUN chmod +x scripts/*
# CMD ["/app/scripts/entrypoint.sh"]

# gunicorn -k eventlet -w 1 --bind 0.0.0.0:5000 --log-config log_config.conf socket_server:app

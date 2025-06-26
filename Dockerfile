FROM python:3.8-slim-buster

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y gcc build-essential libzstd-dev && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --upgrade accelerate
RUN pip uninstall -y transformers accelerate
RUN pip install transformers accelerate

CMD ["python3", "app.py"]
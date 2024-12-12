# app/Dockerfile

FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/manuelm1209/agentocy_test.git .

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/agentocy_test/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
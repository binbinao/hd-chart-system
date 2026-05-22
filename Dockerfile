FROM python:3.11-slim

WORKDIR /app

# Install build dependencies for pyswisseph
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directory for persistent data
RUN mkdir -p /data

ENV HD_DB_PATH=/data/hd_records.db

EXPOSE 18090

CMD ["python", "-m", "hd_api.main"]

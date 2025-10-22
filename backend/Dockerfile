# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for opencv and ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg build-essential libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install backend deps
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy entire repo (needed for local editable install of ImageAI lib)
COPY . /app

# Install local ImageAI library in editable mode
RUN pip install --no-cache-dir -e .

# Expose port and default command
EXPOSE 8000

# Create data directories
RUN mkdir -p /app/backend/app/data/uploads /app/backend/app/data/outputs

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

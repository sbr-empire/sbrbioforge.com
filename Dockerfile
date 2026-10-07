# Multi-stage build for Flutter + Python Flask app
# Stage 1: Build Flutter web app
FROM ghcr.io/cirruslabs/flutter:stable AS flutter-builder
WORKDIR /flutter-src

# Install dependencies
COPY pubspec.yaml pubspec.lock* ./
RUN flutter pub get

# Copy entire project
COPY . .

# Build web release
RUN flutter build web --release --web-renderer canvaskit

# Stage 2: Python Flask server
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python app
COPY app.py database.py ./

# Copy built Flutter web app from stage 1
COPY --from=flutter-builder /flutter-src/build/web ./build/web

# Health check for Cloud Run
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8080}/health').read()"

# Expose port (Cloud Run will override)
EXPOSE 8080

# Run Flask app with gunicorn
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 4 --timeout 120 app:app

FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir flask gunicorn google-cloud-secret-manager google-cloud-storage
COPY . .
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "app:app"]

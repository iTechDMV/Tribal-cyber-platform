# 1. Base image
FROM python:3.11-slim

# 2. Workdir
WORKDIR /app

# 3. Install system deps (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy app code
COPY . /app

# 5. Install Python deps
# Make sure requirements.txt exists and includes Flask, gunicorn, etc.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Expose port for Cloud Run
ENV PORT=8080

# 7. Gunicorn entrypoint (Flask app named "app" in app.py)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

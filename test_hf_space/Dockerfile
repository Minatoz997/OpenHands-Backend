# Dockerfile for Hugging Face Spaces
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p /tmp/openhands /tmp/cache && \
    chmod 755 /tmp/openhands /tmp/cache

# Set environment variables for HF Spaces
ENV PYTHONPATH=/app
ENV OPENHANDS_RUNTIME=local
ENV PORT=7860
ENV HOST=0.0.0.0
ENV CORS_ALLOWED_ORIGINS=*
ENV FILE_STORE_PATH=/tmp/openhands
ENV CACHE_DIR=/tmp/cache

# Expose port (HF Spaces requires 7860)
EXPOSE 7860

# Run the application
CMD ["python", "app_hf.py"]
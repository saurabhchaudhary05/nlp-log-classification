FROM python:3.11-slim

WORKDIR /app

# HuggingFace caches should go to /tmp (writable on most PaaS)
ENV HF_HOME=/tmp/hf \
    TRANSFORMERS_CACHE=/tmp/hf/transformers \
    SENTENCE_TRANSFORMERS_HOME=/tmp/hf/sentence-transformers \
    HF_HUB_CACHE=/tmp/hf/hub

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads outputs /tmp/hf/transformers /tmp/hf/sentence-transformers /tmp/hf/hub

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "app:app"]

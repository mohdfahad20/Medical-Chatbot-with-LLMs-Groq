# Use official Python base image
FROM python:3.10.0-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal set)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Copy requirements
COPY requirements.txt .

# Install PyTorch CPU-only version first (much smaller than CUDA version)
RUN pip install --no-cache-dir \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies with aggressive cleanup
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip && \
    # Remove unnecessary files from installed packages
    find /usr/local/lib/python3.10 -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.10 -type d -name "test" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.10 -name "*.pyc" -delete && \
    find /usr/local/lib/python3.10 -name "*.pyo" -delete && \
    find /usr/local/lib/python3.10 -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Copy only essential project files
COPY app.py .
COPY config.py .
COPY rate_limiter.py .

# Copy source code
COPY src/ ./src/

# Copy Streamlit config (exclude secrets.toml via .dockerignore)
COPY .streamlit/config.toml ./.streamlit/

# Copy data and pre-built FAISS index
COPY data/Medical_book.pdf ./data/
COPY faiss_index/ ./faiss_index/

# Expose the port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py"]
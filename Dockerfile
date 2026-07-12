FROM python:3.11-slim

# Python runtime configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# All following commands run from /app
WORKDIR /app

# Copy dependency file first so Docker can cache this layer
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create a non-root application user
RUN useradd --create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

# Document the port used by Streamlit
EXPOSE 8501

# Check whether Streamlit is responding
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=30s \
    --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health', timeout=3)"

# Start the Streamlit dashboard
CMD ["streamlit", "run", "dashboard/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true", "--browser.gatherUsageStats=false"]
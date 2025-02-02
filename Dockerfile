FROM python:3.9-slim as build

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy only necessary files from build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .

# Create non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app && \
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app/logs

USER appuser

# Set environment variables
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO
ENV MAX_CONNECTIONS=50
ENV REDIS_URL=redis://redis:6379
ENV METRICS_PORT=9090

# Expose ports
EXPOSE 8000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "main.py"]
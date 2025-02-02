# Email Validator Deployment Guide

## Prerequisites
- Python 3.8+
- Redis server
- Docker (optional)

## Installation

### Using Python
1. Clone the repository
```bash
git clone https://github.com/yourusername/email-validator.git
cd email-validator
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the service
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker
1. Build the image
```bash
docker build -t email-validator .
```

2. Run with Docker
```bash
docker run -d \
  -p 8000:8000 \
  -e EMAIL_VALIDATOR_REDIS_HOST=your-redis-host \
  email-validator
```

### Using Docker Compose
1. Start all services
```bash
docker-compose up -d
```

## Configuration
See [Configuration Guide](./configuration.md) for available settings.

## Monitoring

### Prometheus Metrics
Metrics are available at `/metrics` endpoint. Configure Prometheus to scrape this endpoint.

Example Prometheus config:
```yaml
scrape_configs:
  - job_name: 'email-validator'
    static_configs:
      - targets: ['localhost:9090']
```

### Health Checks
Health endpoint is available at `/api/v1/health`.

## Scaling
The service can be scaled horizontally by:
1. Increasing API workers
2. Running multiple instances behind a load balancer
3. Scaling Redis for improved caching

## Security Considerations
1. Configure rate limiting
2. Set up authentication if needed
3. Use HTTPS in production
4. Keep dependencies updated
5. Monitor for abuse

## Troubleshooting
1. Check logs: `docker logs email-validator`
2. Verify Redis connection
3. Test DNS resolution
4. Monitor SMTP connection pools
5. Check rate limiting status
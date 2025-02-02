# Email Validator Service

A high-performance, enterprise-grade email validation service with comprehensive validation features including RFC 5322 compliance, DNS verification, and SMTP validation.

## Features

- RFC 5322 compliant email validation
- DNS verification with MX record lookup
- SMTP verification with connection pooling
- Disposable email detection
- Internationalized email support (IDNA 2008)
- High performance with caching and connection pooling
- Comprehensive monitoring with Prometheus/Grafana
- Kubernetes-ready deployment
- Extensive test coverage

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Kubernetes cluster (for production deployment)
- AWS account (for production deployment)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/your-org/email-validator.git
cd email-validator
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment template and configure:
```bash
cp .env.template .env
# Edit .env with your configuration
```

5. Run with Docker Compose:
```bash
docker-compose up -d
```

### Running Tests

```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## Deployment

### Staging Deployment

```bash
./scripts/deploy.sh staging
```

### Production Deployment

1. Configure AWS credentials
2. Update Kubernetes configurations
3. Deploy:
```bash
./scripts/deploy.sh production
```

## Monitoring

Service metrics are available at `/metrics` endpoint and can be collected by Prometheus.

### Setting up monitoring:

```bash
./scripts/initialize_monitoring.sh
```

Access Grafana dashboard at: http://localhost:3000

## Contributing

1. Fork the repository
2. Create your feature branch
3. Run tests and linting
4. Submit pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Installation Guide

## Windows Installation

1. Prerequisites
   - Python 3.8 or higher
   - Git (optional, for cloning the repository)
   - Docker Desktop (optional, for running with Docker)

2. Download and Setup
   ```powershell
   # Clone the repository (or download ZIP from repository)
   git clone <repository-url>
   cd email-validator

   # Create a virtual environment
   python -m venv venv
   .\venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. Configuration
   - Copy `config/system.json.example` to `config/system.json` (if exists)
   - Update configuration values as needed

4. Running the Application
   ```powershell
   # Direct Python execution
   python main.py

   # Or using Docker
   docker-compose up -d
   ```

## Linux Installation

1. Prerequisites
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git

   # CentOS/RHEL
   sudo dnf install python3 python3-pip git
   ```

2. Setup
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd email-validator

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. Configuration
   ```bash
   # Set up configuration
   cp config/system.json.example config/system.json  # if exists
   # Edit config/system.json with your preferred editor
   ```

4. Running
   ```bash
   # Direct execution
   python main.py

   # Or with Docker
   docker-compose up -d
   ```

## macOS Installation

1. Prerequisites
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install Python and Git
   brew install python git
   ```

2. Setup
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd email-validator

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. Configuration
   ```bash
   # Set up configuration
   cp config/system.json.example config/system.json  # if exists
   # Edit config/system.json with your preferred editor
   ```

4. Running
   ```bash
   # Direct execution
   python main.py

   # Or with Docker
   docker-compose up -d
   ```

## Docker Installation (All Platforms)

1. Prerequisites
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - Install [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop for Windows and macOS)

2. Setup
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd email-validator
   ```

3. Configuration
   - Update any necessary configuration in `docker-compose.yml`
   - Configure environment variables if needed

4. Running
   ```bash
   # Build and start containers
   docker-compose up -d

   # View logs
   docker-compose logs -f
   ```

## Troubleshooting

For common issues and solutions, please refer to our [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## Additional Resources

- [Usage Documentation](docs/USAGE.md)
- [Configuration Guide](docs/configuration.md)
- [API Documentation](docs/api.md)
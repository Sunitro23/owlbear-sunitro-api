# Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Dark Souls API to various environments, from local development to production servers.

## Prerequisites

Before deploying, ensure you have:

- Python 3.9+ installed
- pip package manager
- Git (for version control and deployment)
- Appropriate permissions for your target environment

## Environment Setup

### Local Development

1. **Clone the repository**:
```bash
git clone <repository-url>
cd darksouls_api
```

2. **Create a virtual environment**:
```bash
# Using venv (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the development server**:
```bash
# Option 1: Using the main.py entry point (recommended)
python main.py

# Option 2: Direct uvicorn command
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Using uvicorn directly
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Environment

#### Option 1: Docker Deployment

1. **Build the Docker image**:
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and run**:
```bash
# Build image
docker build -t darksouls-api .

# Run container
docker run -p 8000:8000 darksouls-api

# Run with persistent storage
docker run -p 8000:8000 -v ./data:/app/data darksouls-api
```

3. **Docker Compose for production**:
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### Option 2: Traditional Server Deployment

1. **Install Python and dependencies**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip
```

2. **Set up the application**:
```bash
# Create application user
sudo useradd --system --shell /bin/bash darksouls

# Create directories
sudo mkdir -p /opt/darksouls_api
sudo chown darksouls:darksouls /opt/darksouls_api

# Clone or copy application
sudo -u darksouls git clone <repository-url> /opt/darksouls_api

# Set up virtual environment
cd /opt/darksouls_api
sudo -u darksouls python3 -m venv venv
source venv/bin/activate
sudo -u darksouls pip install -r requirements.txt
```

3. **Configure systemd service**:
```ini
# /etc/systemd/system/darksouls-api.service
[Unit]
Description=Dark Souls API
After=network.target

[Service]
Type=exec
User=darksouls
Group=darksouls
WorkingDirectory=/opt/darksouls_api
Environment="PATH=/opt/darksouls_api/venv/bin"
ExecStart=/opt/darksouls_api/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

4. **Enable and start the service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable darksouls-api
sudo systemctl start darksouls-api
```

## Configuration

### Environment Variables

The API supports several environment variables for configuration:

```bash
# Application settings
ENVIRONMENT=production          # Environment mode (development, staging, production)
LOG_LEVEL=info                  # Logging level (debug, info, warning, error)
DEBUG=false                     # Enable debug mode

# Server settings
HOST=0.0.0.0                    # Host to bind to
PORT=8000                       # Port to bind to
WORKERS=4                       # Number of worker processes

# Database settings
STORAGE_PATH=./data             # Path for JSON storage
BACKUP_INTERVAL=3600            # Backup interval in seconds

# Security settings
CORS_ORIGINS=http://localhost   # Allowed CORS origins
RATE_LIMIT=100                  # Requests per minute per IP
```

### Configuration File

Create a `.env` file in the project root:

```bash
# .env
ENVIRONMENT=production
LOG_LEVEL=info
DEBUG=false
HOST=0.0.0.0
PORT=8000
WORKERS=4
STORAGE_PATH=./data
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT=100
```

## Production Considerations

### Security

1. **Use HTTPS**:
```bash
# Using Let's Encrypt with Certbot
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Configure reverse proxy (nginx example)
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **Enable CORS properly**:
```python
# In src/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. **Rate limiting**:
```python
# Add rate limiting middleware
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/characters")
@limiter.limit("100/minute")
async def get_characters():
    return character_service.get_all_characters()
```

### Performance Optimization

1. **Use multiple workers**:
```bash
# Using Gunicorn
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Uvicorn with multiple workers
uvicorn src.api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

2. **Enable compression**:
```python
# In src/api/main.py
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

3. **Database optimization**:
- Consider switching from JSON storage to a proper database (PostgreSQL, MongoDB)
- Implement caching for frequently accessed data
- Use database connection pooling

### Monitoring and Logging

1. **Structured logging**:
```python
import logging
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}
```

2. **Metrics collection**:
```python
from prometheus_client import Counter, Histogram, start_http_server
import time

REQUEST_COUNT = Counter('requests_total', 'Total requests')
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.inc()
    REQUEST_DURATION.observe(duration)
    
    return response
```

3. **Health checks**:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
```

## Cloud Deployment

### AWS Deployment

1. **Using AWS Elastic Beanstalk**:
```yaml
# .ebextensions/python.config
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: src.api.main:app
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: static
```

2. **Using AWS ECS**:
```yaml
# task-definition.json
{
  "family": "darksouls-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "your-account.dkr.ecr.region.amazonaws.com/darksouls-api:latest",
      "portMappings": [{"containerPort": 8000}],
      "environment": [
        {"name": "ENVIRONMENT", "value": "production"}
      ]
    }
  ]
}
```

### Google Cloud Platform

1. **Using Cloud Run**:
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/darksouls-api:$COMMIT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/darksouls-api:$COMMIT_SHA']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'darksouls-api',
           '--image', 'gcr.io/$PROJECT_ID/darksouls-api:$COMMIT_SHA',
           '--region', 'us-central1',
           '--platform', 'managed',
           '--allow-unauthenticated']
```

2. **Deploy command**:
```bash
gcloud run deploy darksouls-api \
  --image gcr.io/your-project/darksouls-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Deployment

1. **Using Azure App Service**:
```yaml
# azure-pipelines.yml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'

- script: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
  displayName: 'Install dependencies'

- task: AzureWebApp@1
  inputs:
    azureSubscription: 'your-subscription'
    appName: 'darksouls-api'
    package: '$(System.DefaultWorkingDirectory)'
```

## Backup and Recovery

### Automated Backups

1. **Create backup script**:
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/darksouls"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/darksouls_backup_$DATE.tar.gz"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_FILE ./data ./logs

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

2. **Schedule with cron**:
```bash
# Add to crontab (crontab -e)
0 2 * * * /path/to/backup.sh
```

### Database Migration

1. **Export data**:
```python
import json
from src.database.repository import character_repository

def export_data():
    characters = character_repository.get_all_characters()
    with open('backup.json', 'w') as f:
        json.dump(characters, f, indent=2)
```

2. **Import data**:
```python
def import_data():
    with open('backup.json', 'r') as f:
        data = json.load(f)
    
    for char_id, char_data in data.items():
        character_repository.storage.save({char_id: char_data})
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
# Check what's using the port
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>
```

2. **Permission denied**:
```bash
# Fix file permissions
sudo chown -R $USER:$USER /path/to/project
sudo chmod -R 755 /path/to/project
```

3. **Import errors**:
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Monitoring Commands

1. **Check service status**:
```bash
# Systemd
sudo systemctl status darksouls-api

# Docker
docker ps
docker logs <container-id>
```

2. **Monitor logs**:
```bash
# Follow logs
tail -f /var/log/darksouls-api.log

# Docker logs
docker logs -f <container-id>
```

3. **Check resource usage**:
```bash
# CPU and memory
top
htop

# Disk usage
df -h
du -sh /path/to/data
```

## Scaling

### Horizontal Scaling

1. **Load balancer configuration**:
```nginx
# nginx.conf
upstream api_backend {
    server 192.168.1.100:8000;
    server 192.168.1.101:8000;
    server 192.168.1.102:8000;
}

server {
    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **Database considerations**:
- Use a shared database (PostgreSQL, MongoDB)
- Implement proper locking mechanisms
- Consider read replicas for high read traffic

### Vertical Scaling

1. **Increase resources**:
- More CPU cores for better parallel processing
- More RAM for caching and larger datasets
- Faster storage (SSD) for better I/O performance

2. **Optimize application**:
- Use async/await for I/O operations
- Implement caching strategies
- Optimize database queries

This deployment guide covers the essential aspects of deploying the Dark Souls API to various environments. Always test your deployment thoroughly before going live with production data.

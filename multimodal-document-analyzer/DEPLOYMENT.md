"""
Deployment guide and setup instructions.
"""

# DEPLOYMENT GUIDE FOR MULTIMODAL DOCUMENT ANALYZER

## Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/yourusername/multimodal-document-analyzer.git
cd multimodal-document-analyzer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -m nltk.downloader punkt stopwords

# 5. Run application
streamlit run app.py
```

Access at: http://localhost:8501


## Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

### Option 2: Standalone Docker

```bash
# Build
docker build -t document-analyzer:latest .

# Run
docker run -p 8501:8501 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/reports:/app/reports \
  -e STREAMLIT_SERVER_HEADLESS=true \
  document-analyzer:latest
```


## Cloud Deployment

### Streamlit Cloud

1. Push to GitHub:
```bash
git push origin main
```

2. Go to https://share.streamlit.io
3. Connect GitHub repository
4. Select main file: `app.py`
5. Click "Deploy"

Environment variables in Streamlit Cloud:
```
DATABASE_PATH=/tmp/analyzer.db
UPLOADS_DIR=/tmp/uploads
REPORTS_DIR=/tmp/reports
LOG_LEVEL=INFO
```

### Heroku Deployment

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Add buildpacks
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/jontewks/puppeteer-buildpack.git

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### AWS Deployment (ECS/Fargate)

```bash
# Create ECR repository
aws ecr create-repository --repository-name document-analyzer

# Build and push
docker build -t document-analyzer:latest .
docker tag document-analyzer:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/document-analyzer:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/document-analyzer:latest

# Create ECS task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Deploy to ECS Fargate
aws ecs create-service --cluster your-cluster --service-name document-analyzer \
  --task-definition document-analyzer:1 --desired-count 1 --launch-type FARGATE
```

### Google Cloud Run Deployment

```bash
# Authenticate
gcloud auth login

# Build and deploy
gcloud run deploy document-analyzer \
  --source . \
  --platform managed \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600
```


## Production Setup

### 1. Environment Variables (.env)

```env
# Database
DATABASE_PATH=/data/analyzer.db

# OCR
USE_EASYOCR=true
OCR_LANGUAGES=en,es,fr

# File Handling
MAX_FILE_SIZE_MB=500
UPLOADS_DIR=/data/uploads
REPORTS_DIR=/data/reports

# Models
MODEL_DEVICE=cuda  # Use GPU if available

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/document-analyzer/app.log

# Security
SESSION_TIMEOUT_MINUTES=60
```

### 2. Database Setup

```bash
# Initialize database
python -c "from database.db import DatabaseManager; DatabaseManager()"

# Backup database
cp analyzer.db analyzer.db.backup
```

### 3. SSL/HTTPS Configuration

Create `ssl_config.py`:
```python
import streamlit as st

# Configure HTTPS
st.session_state.ssl_keyfile = "/path/to/key.pem"
st.session_state.ssl_certfile = "/path/to/cert.pem"
```

### 4. Reverse Proxy (Nginx)

```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Systemd Service (Linux)

Create `/etc/systemd/system/document-analyzer.service`:
```ini
[Unit]
Description=Multimodal Document Analyzer
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/document-analyzer
Environment="PATH=/opt/document-analyzer/venv/bin"
ExecStart=/opt/document-analyzer/venv/bin/streamlit run app.py \
    --server.port=8501 \
    --server.address=127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable document-analyzer
sudo systemctl start document-analyzer
```

### 6. Monitoring

```bash
# Monitor CPU and memory
docker stats document-analyzer

# Log rotation
# Use logrotate for Linux
```


## Performance Optimization

### 1. GPU Acceleration

```bash
# Install CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Set in config.py
MODEL_DEVICE=cuda
```

### 2. Model Optimization

```python
# Use quantized models
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "model-name",
    load_in_8bit=True
)
```

### 3. Caching

```python
import streamlit as st

@st.cache_data
def load_model():
    # Load model once
    return model

@st.cache_resource
def get_database():
    # Get database connection
    return DatabaseManager()
```


## Scaling

### Multi-instance Deployment

Use Kubernetes for orchestration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: document-analyzer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: document-analyzer
  template:
    metadata:
      labels:
        app: document-analyzer
    spec:
      containers:
      - name: analyzer
        image: document-analyzer:latest
        ports:
        - containerPort: 8501
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
          requests:
            cpu: "1"
            memory: "2Gi"
```


## Troubleshooting

### Memory Issues
```bash
# Increase available memory
docker run -m 4g document-analyzer:latest

# Monitor memory usage
docker stats
```

### Port Already in Use
```bash
# Change port
streamlit run app.py --server.port=8502

# Or kill process using port
sudo lsof -i :8501
sudo kill -9 <PID>
```

### Database Lock
```bash
# Check database locks
sqlite3 analyzer.db "PRAGMA integrity_check;"

# Reset database
rm analyzer.db
python -c "from database.db import DatabaseManager; DatabaseManager()"
```


## Maintenance

### Regular Backups

```bash
#!/bin/bash
# Backup daily at 2 AM
0 2 * * * cp analyzer.db /backups/analyzer_$(date +%Y%m%d).db.bak
```

### Log Cleanup

```bash
#!/bin/bash
# Remove logs older than 30 days
find /var/log/document-analyzer -name "*.log" -mtime +30 -delete
```

### Database Optimization

```sql
-- Vacuum database to optimize size
VACUUM;

-- Analyze query performance
ANALYZE;
```


## Security Checklist

- [ ] Change default passwords
- [ ] Enable HTTPS/SSL
- [ ] Set strong database encryption
- [ ] Implement rate limiting
- [ ] Enable logging and monitoring
- [ ] Regular security updates
- [ ] Firewall configuration
- [ ] File upload validation
- [ ] API authentication (if enabled)
- [ ] Data backup and recovery plan


## Additional Resources

- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)

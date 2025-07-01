# UniLLM Production Deployment Guide

## 🚀 Production Deployment Options

### Option 1: Cloud Deployment (Recommended)

#### **AWS Deployment**
```bash
# 1. Set up EC2 instance
aws ec2 run-instances --image-id ami-0c02fb55956c7d316 --instance-type t3.medium --key-name your-key

# 2. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx redis-server

# 3. Clone and setup UniLLM
git clone <your-repo>
cd singlemodel/api_gateway
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_phase2.txt

# 4. Configure environment variables
cp env_example.txt .env
# Edit .env with your production settings
```

#### **Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements_phase2.txt .
RUN pip install -r requirements_phase2.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main_phase2:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Option 2: Local Production Setup

#### **Environment Configuration**
```bash
# Production environment variables
export UNILLM_ENV=production
export SECRET_KEY=your-super-secure-secret-key
export DATABASE_URL=postgresql://user:pass@localhost/unillm
export REDIS_URL=redis://localhost:6379

# API Keys for providers
export OPENAI_API_KEY=your-openai-key
export ANTHROPIC_API_KEY=your-anthropic-key
export GOOGLE_API_KEY=your-google-key
```

#### **Database Setup**
```bash
# PostgreSQL (recommended for production)
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb unillm
sudo -u postgres createuser unillm_user

# Update database.py to use PostgreSQL
```

### Option 3: Serverless Deployment

#### **AWS Lambda + API Gateway**
```yaml
# serverless.yml
service: unillm-api

provider:
  name: aws
  runtime: python3.10
  region: us-east-1

functions:
  api:
    handler: handler.main
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

## 🔧 Production Configuration

### Security Enhancements
```python
# main_phase2.py - Production settings
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Enable HTTPS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting & Monitoring
```python
# Enhanced rate limiting
RATE_LIMIT_PER_MINUTE = 60
RATE_LIMIT_PER_HOUR = 1000
RATE_LIMIT_PER_DAY = 10000

# Add monitoring
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Database Optimization
```python
# database.py - Production database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unillm.db")

# Add connection pooling
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

## 📊 Monitoring & Analytics

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0",
        "database": "connected",
        "redis": "connected",
        "uptime": get_uptime()
    }
```

### Usage Analytics
```python
@app.get("/admin/analytics")
async def get_analytics(admin: User = Depends(require_admin)):
    return {
        "total_users": get_total_users(),
        "active_users": get_active_users(),
        "total_requests": get_total_requests(),
        "revenue": get_total_revenue(),
        "popular_models": get_popular_models()
    }
```

## 🔐 Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Add request validation
- [ ] Implement API key rotation
- [ ] Set up monitoring and alerts
- [ ] Regular security audits
- [ ] Database backups
- [ ] Environment variable management

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ALB, Nginx)
- Database read replicas
- Redis cluster for caching
- CDN for static assets

### Performance Optimization
- Database indexing
- Query optimization
- Caching strategies
- Async processing
- Connection pooling

## 🚨 Monitoring & Alerts

### Key Metrics to Monitor
- API response times
- Error rates
- User growth
- Revenue metrics
- System resources
- Database performance

### Alert Setup
```python
# Example alert configuration
ALERT_THRESHOLDS = {
    "error_rate": 0.05,  # 5%
    "response_time": 2000,  # 2 seconds
    "cpu_usage": 0.8,  # 80%
    "memory_usage": 0.85  # 85%
}
```

## 📋 Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrated and tested
- [ ] SSL certificates installed
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Team access configured
- [ ] Rollback plan ready
- [ ] Performance benchmarks established 
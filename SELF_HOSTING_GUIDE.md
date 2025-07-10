# 🏠 UniLLM Self-Hosting Guide

## Overview
This guide will help you set up and run your own instance of UniLLM on your infrastructure. Perfect for developers who want full control over their LLM API gateway with their own API keys.

## 🎯 Why Self-Host?

- **🔒 Privacy**: Your data never leaves your infrastructure
- **💰 Cost Control**: No markup on API calls, pay only what providers charge
- **⚡ Performance**: Lower latency, no shared infrastructure
- **🔧 Customization**: Modify the code to fit your specific needs
- **📊 Full Analytics**: Complete control over usage tracking and billing

## 🚀 Quick Start (5 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/unillm
cd unillm
```

### 2. Set Up Backend
```bash
cd api_gateway

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env_example.txt .env

# Edit .env with your API keys
nano .env
```

### 3. Configure Your API Keys
Edit `.env` file:
```bash
# Required API Keys
OPENAI_API_KEY=sk-proj-your-openai-key
ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key
GEMINI_API_KEY=your-gemini-key
MISTRAL_API_KEY=your-mistral-key
COHERE_API_KEY=your-cohere-key

# Security
SECRET_KEY=your-secure-secret-key-here

# Database (SQLite for local, PostgreSQL for production)
DATABASE_URL=sqlite:///unillm.db

# CORS (for frontend)
CORS_ORIGINS=http://localhost:3000
FRONTEND_URL=http://localhost:3000
```

### 4. Start the Backend
```bash
python main_phase2.py
```

Your API gateway is now running at `http://localhost:8000`! 🎉

### 5. Set Up Frontend (Optional)
```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm start
```

Access your dashboard at `http://localhost:3000`

## 🔧 Production Deployment

### Option 1: Docker (Recommended)

#### Create Dockerfile
```dockerfile
# api_gateway/Dockerfile
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

# Start the application
CMD ["uvicorn", "main_phase2:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create docker-compose.yml
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./api_gateway
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - COHERE_API_KEY=${COHERE_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
      - CORS_ORIGINS=${CORS_ORIGINS}
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_BASE_URL=${API_BASE_URL}
    depends_on:
      - api
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
      - frontend
    restart: unless-stopped
```

#### Deploy with Docker
```bash
# Create .env file
cp env_example.txt .env
# Edit with your API keys

# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option 2: VPS Deployment

#### 1. Set Up Your Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, Node.js, and PostgreSQL
sudo apt install python3 python3-pip nodejs npm postgresql postgresql-contrib nginx

# Install certbot for SSL
sudo apt install certbot python3-certbot-nginx
```

#### 2. Set Up PostgreSQL
```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE unillm;
CREATE USER unillm_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE unillm TO unillm_user;
\q

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://unillm_user:your_password@localhost/unillm
```

#### 3. Deploy Application
```bash
# Clone repository
git clone https://github.com/yourusername/unillm
cd unillm

# Set up backend
cd api_gateway
pip3 install -r requirements.txt
pip3 install psycopg2-binary

# Set up frontend
cd ../frontend
npm install
npm run build
```

#### 4. Configure Nginx
```nginx
# /etc/nginx/sites-available/unillm
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/unillm/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 5. Set Up Systemd Services
```bash
# /etc/systemd/system/unillm-api.service
[Unit]
Description=UniLLM API Gateway
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/unillm/api_gateway
Environment=PATH=/usr/local/bin
ExecStart=/usr/local/bin/uvicorn main_phase2:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start services
sudo systemctl enable unillm-api
sudo systemctl start unillm-api
sudo systemctl enable nginx
sudo systemctl start nginx
```

#### 6. Set Up SSL
```bash
sudo certbot --nginx -d your-domain.com
```

## 🔑 Getting Your First API Key

### 1. Register a User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-secure-password"
  }'
```

### 2. Login to Get API Key
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-secure-password"
  }'
```

### 3. Use Your API Key
```python
from unillm import UniLLM

client = UniLLM(
    api_key="your-api-key-from-login",
    base_url="http://localhost:8000"  # or your domain
)

response = client.chat(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content)
```

## 🎨 Customization Options

### 1. Modify Pricing
Edit `api_gateway/database.py`:
```python
# Remove markup for self-hosting
def calculate_cost(provider: str, model: str, tokens: int) -> float:
    base_cost = PROVIDER_COSTS.get(provider, {}).get(model, 0.01)
    # No markup for self-hosting
    return (tokens / 1000) * base_cost
```

### 2. Add Custom Models
Edit `api_gateway/database.py`:
```python
PROVIDER_COSTS = {
    "openai": {
        "gpt-3.5-turbo": 0.002,
        "gpt-4": 0.03,
        "your-custom-model": 0.01,  # Add your models
    },
    # ... other providers
}
```

### 3. Custom Authentication
Modify `api_gateway/auth.py` to integrate with your existing auth system.

### 4. Custom Dashboard
Modify `frontend/src/` to match your branding and requirements.

## 📊 Monitoring & Analytics

### 1. Built-in Analytics
- Access dashboard at `http://your-domain.com`
- View usage statistics, costs, and request history
- Monitor API performance and errors

### 2. Logs
```bash
# View API logs
sudo journalctl -u unillm-api -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 3. Database Queries
```sql
-- View usage statistics
SELECT 
    provider,
    model,
    COUNT(*) as requests,
    SUM(tokens_used) as total_tokens,
    SUM(cost) as total_cost
FROM usage_logs 
GROUP BY provider, model;

-- View user activity
SELECT 
    u.email,
    COUNT(ul.id) as requests,
    SUM(ul.cost) as total_cost
FROM users u
LEFT JOIN usage_logs ul ON u.id = ul.user_id
GROUP BY u.id, u.email;
```

## 🔒 Security Best Practices

### 1. Environment Variables
```bash
# Never commit API keys to version control
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
```

### 2. Firewall Configuration
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 3. Regular Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update Python packages
pip install --upgrade -r requirements.txt

# Update Node.js packages
npm update
```

### 4. Backup Strategy
```bash
# Backup database
pg_dump unillm > backup_$(date +%Y%m%d).sql

# Backup configuration
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env nginx.conf
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Install missing dependencies
pip install -r requirements.txt
```

#### 2. Database connection issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U unillm_user -d unillm
```

#### 3. CORS errors
```bash
# Update CORS_ORIGINS in .env
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
```

#### 4. API key authentication fails
```bash
# Check user exists
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer your-api-key"
```

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/unillm/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/unillm/discussions)
- **Documentation**: Check the main [README.md](README.md)

## 🎉 You're Ready!

Your self-hosted UniLLM instance is now running! You have:

- ✅ **Full control** over your LLM API gateway
- ✅ **No markup** on API calls
- ✅ **Complete privacy** - your data stays on your infrastructure
- ✅ **Customizable** dashboard and functionality
- ✅ **Production-ready** deployment

**Next steps:**
1. Test your API with the examples above
2. Customize the dashboard to match your needs
3. Set up monitoring and alerts
4. Consider setting up automated backups

Happy coding! 🚀 
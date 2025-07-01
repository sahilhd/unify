# 🚀 UniLLM Production Deployment Guide

## Overview
This guide will help you deploy UniLLM to production so others can create accounts and use your unified API for OpenAI and Anthropic.

## Quick Start (Railway - Recommended)

### Step 1: Prepare Your Codebase
```bash
# Run the deployment preparation script
python deploy.py
```

### Step 2: Deploy to Railway
1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub repository**
3. **Create a new project** from your repository
4. **Set environment variables** in Railway dashboard:
   ```
   ENVIRONMENT=production
   SECRET_KEY=your-generated-secret-key
   OPENAI_API_KEY=sk-proj-your-openai-key
   ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key
   CORS_ORIGINS=https://your-frontend-domain.com
   FRONTEND_URL=https://your-frontend-domain.com
   ```
5. **Deploy** - Railway will automatically build and deploy your app

### Step 3: Configure Custom Domain
1. Go to your Railway project settings
2. Add a custom domain (e.g., `api.yourdomain.com`)
3. Update your DNS settings
4. Update `CORS_ORIGINS` with your new domain

## Alternative Platforms

### Render Deployment
1. **Sign up** at [render.com](https://render.com)
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure build settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd api_gateway && python main_phase2.py`
5. **Set environment variables** (same as Railway)
6. **Deploy**

### Heroku Deployment
1. **Sign up** at [heroku.com](https://heroku.com)
2. **Install Heroku CLI**
3. **Create app**:
   ```bash
   heroku create your-unillm-app
   ```
4. **Set environment variables**:
   ```bash
   heroku config:set ENVIRONMENT=production
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set OPENAI_API_KEY=your-openai-key
   heroku config:set ANTHROPIC_API_KEY=your-anthropic-key
   ```
5. **Deploy**:
   ```bash
   git push heroku main
   ```

## Frontend Deployment

### Option 1: Vercel (Recommended)
1. **Sign up** at [vercel.com](https://vercel.com)
2. **Import your repository**
3. **Configure build settings**:
   - Framework Preset: Create React App
   - Build Command: `npm run build`
   - Output Directory: `build`
4. **Set environment variables**:
   ```
   REACT_APP_API_URL=https://your-api-domain.com
   ```
5. **Deploy**

### Option 2: Netlify
1. **Sign up** at [netlify.com](https://netlify.com)
2. **Import your repository**
3. **Configure build settings**:
   - Build Command: `cd frontend && npm run build`
   - Publish Directory: `frontend/build`
4. **Set environment variables** (same as Vercel)
5. **Deploy**

## Environment Variables

### Required Variables
```bash
# Environment
ENVIRONMENT=production
DEBUG=false

# Security
SECRET_KEY=your-secure-secret-key

# API Keys
OPENAI_API_KEY=sk-proj-your-openai-key
ANTHROPIC_API_KEY=sk-ant-api03-your-anthropic-key

# CORS
CORS_ORIGINS=https://your-frontend-domain.com
FRONTEND_URL=https://your-frontend-domain.com
```

### Optional Variables
```bash
# Database (use PostgreSQL for production)
DATABASE_URL=postgresql://user:pass@host:port/db

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
DAILY_QUOTA=10000

# Billing
DEFAULT_CREDITS=10.0
MIN_CREDITS_FOR_REQUEST=0.001
```

## Database Setup

### SQLite (Development)
- ✅ Already configured
- ✅ Works out of the box
- ❌ Not recommended for production

### PostgreSQL (Production)
1. **Create PostgreSQL database** (Railway/Render/Heroku provide this)
2. **Update DATABASE_URL**:
   ```
   DATABASE_URL=postgresql://user:pass@host:port/db
   ```
3. **Install PostgreSQL adapter**:
   ```bash
   pip install psycopg2-binary
   ```

## Security Checklist

### ✅ Completed
- [x] Secure secret key generation
- [x] CORS configuration
- [x] Rate limiting
- [x] Input validation
- [x] API key authentication

### 🔄 To Implement
- [ ] HTTPS enforcement
- [ ] Request logging
- [ ] Error monitoring
- [ ] Backup strategy
- [ ] SSL certificate management

## Testing Your Deployment

### 1. Health Check
```bash
curl https://your-api-domain.com/health
```

### 2. User Registration
```bash
curl -X POST https://your-api-domain.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### 3. API Usage
```bash
curl -X POST https://your-api-domain.com/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Monitoring & Maintenance

### Logs
- Railway: Built-in logging dashboard
- Render: Logs tab in dashboard
- Heroku: `heroku logs --tail`

### Performance
- Monitor response times
- Track API usage
- Watch for errors
- Monitor database performance

### Updates
- Keep dependencies updated
- Monitor security advisories
- Regular backups
- Test updates in staging

## Troubleshooting

### Common Issues

#### 1. CORS Errors
**Problem**: Frontend can't connect to API
**Solution**: Update `CORS_ORIGINS` with your frontend domain

#### 2. Database Connection
**Problem**: Database connection failed
**Solution**: Check `DATABASE_URL` and database credentials

#### 3. API Key Issues
**Problem**: Invalid API key errors
**Solution**: Verify environment variables are set correctly

#### 4. Build Failures
**Problem**: Deployment fails during build
**Solution**: Check requirements.txt and Python version

### Getting Help
1. Check the logs in your deployment platform
2. Test locally with production environment variables
3. Verify all environment variables are set
4. Check network connectivity and DNS settings

## Success Metrics
- ✅ Users can register successfully
- ✅ API calls work with new API keys
- ✅ Dashboard is accessible
- ✅ Usage tracking works
- ✅ Billing system functions
- ✅ Multi-provider support works

## Next Steps
1. **Set up monitoring** (Sentry, LogRocket)
2. **Implement analytics** (Google Analytics, Mixpanel)
3. **Add payment processing** (Stripe, PayPal)
4. **Create admin dashboard**
5. **Set up automated backups**
6. **Implement CI/CD pipeline**

Your UniLLM service is now ready for public use! 🎉 
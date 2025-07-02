# Frontend Deployment Guide

## 🚀 Deploy to Railway

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add frontend deployment config"
git push origin main
```

### Step 2: Create Railway Service
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Choose the `frontend` directory as the source

### Step 3: Configure Environment Variables
Add these environment variables in Railway:
- `REACT_APP_API_BASE_URL`: `https://web-production-70deb.up.railway.app` (your backend URL)

### Step 4: Deploy
Railway will automatically:
1. Install dependencies (`npm install`)
2. Build the app (`npm run build`)
3. Serve static files (`npx serve -s build -l $PORT`)

## 🔧 Alternative: Deploy to Render

### Step 1: Create Render Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Static Site"
3. Connect your GitHub repository
4. Set build command: `npm run build`
5. Set publish directory: `build`

### Step 2: Configure Environment Variables
Add `REACT_APP_API_BASE_URL` with your backend URL.

## 🌐 Custom Domain (Optional)
After deployment, you can add a custom domain in Railway/Render settings.

## ✅ Verification
After deployment, test:
1. Frontend loads without errors
2. Login/registration works
3. Chat functionality connects to backend
4. All dashboard sections work 
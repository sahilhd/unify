#!/usr/bin/env python3
"""
UniLLM Deployment Script
Prepares the application for production deployment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if all required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if required files exist
    required_files = [
        "api_gateway/main_phase2.py",
        "api_gateway/requirements.txt",
        "frontend/package.json",
        "src/unillm/__init__.py"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing required file: {file_path}")
            return False
    
    print("✅ All required files found")
    return True

def generate_secret_key():
    """Generate a secure secret key"""
    import secrets
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create production environment file"""
    print("🔧 Creating production environment file...")
    
    env_content = f"""# UniLLM Production Environment Variables
ENVIRONMENT=production
DEBUG=false

# Security
SECRET_KEY={generate_secret_key()}
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (use PostgreSQL for production)
DATABASE_URL=sqlite:///unillm.db

# API Keys (set these in your deployment platform)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
COHERE_API_KEY=your_cohere_api_key_here

# CORS Configuration
CORS_ORIGINS=https://your-frontend-domain.com,https://your-api-domain.com
FRONTEND_URL=https://your-frontend-domain.com

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
DAILY_QUOTA=10000

# Billing
DEFAULT_CREDITS=10.0
MIN_CREDITS_FOR_REQUEST=0.001

# Logging
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000
"""
    
    with open(".env.production", "w") as f:
        f.write(env_content)
    
    print("✅ Created .env.production file")
    print("⚠️  Remember to update the API keys and domain URLs!")

def build_frontend():
    """Build the React frontend for production"""
    print("🏗️  Building frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install dependencies
    print("📦 Installing frontend dependencies...")
    result = subprocess.run(["npm", "install"], cwd=frontend_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to install frontend dependencies: {result.stderr}")
        return False
    
    # Build for production
    print("🔨 Building frontend for production...")
    result = subprocess.run(["npm", "run", "build"], cwd=frontend_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to build frontend: {result.stderr}")
        return False
    
    print("✅ Frontend built successfully")
    return True

def build_python_package():
    """Build the Python package"""
    print("🐍 Building Python package...")
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Build package
    result = subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to build Python package: {result.stderr}")
        return False
    
    print("✅ Python package built successfully")
    return True

def create_deployment_files():
    """Create deployment-specific files"""
    print("📝 Creating deployment files...")
    
    # Create Procfile for Railway/Heroku
    procfile_content = """web: cd api_gateway && python main_phase2.py
"""
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    # Create runtime.txt for Python version
    runtime_content = "python-3.10.0\n"
    with open("runtime.txt", "w") as f:
        f.write(runtime_content)
    
    # Create requirements.txt for deployment
    requirements_content = """fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
openai==1.3.7
anthropic==0.7.7
google-generativeai==0.3.2
mistralai==0.0.12
cohere==4.37
requests==2.31.0
"""
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    
    print("✅ Deployment files created")

def create_railway_config():
    """Create Railway-specific configuration"""
    print("🚂 Creating Railway configuration...")
    
    railway_json = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "cd api_gateway && python main_phase2.py",
            "healthcheckPath": "/health",
            "healthcheckTimeout": 300,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    import json
    with open("railway.json", "w") as f:
        json.dump(railway_json, f, indent=2)
    
    print("✅ Railway configuration created")

def main():
    """Main deployment preparation function"""
    print("🚀 UniLLM Deployment Preparation")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        sys.exit(1)
    
    # Create production environment file
    create_env_file()
    
    # Build frontend
    if not build_frontend():
        print("❌ Frontend build failed")
        sys.exit(1)
    
    # Build Python package
    if not build_python_package():
        print("❌ Python package build failed")
        sys.exit(1)
    
    # Create deployment files
    create_deployment_files()
    
    # Create Railway config
    create_railway_config()
    
    print("\n🎉 Deployment preparation completed!")
    print("\n📋 Next steps:")
    print("1. Update .env.production with your actual API keys")
    print("2. Update CORS_ORIGINS with your domain URLs")
    print("3. Choose your deployment platform:")
    print("   - Railway: railway.app")
    print("   - Render: render.com")
    print("   - Heroku: heroku.com")
    print("4. Deploy using the platform's instructions")
    print("\n📚 See DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main() 
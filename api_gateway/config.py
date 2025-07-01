"""
Configuration management for UniLLM API Gateway
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///unillm.db")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# CORS Configuration
def get_cors_origins() -> List[str]:
    """Get CORS origins based on environment"""
    if ENVIRONMENT == "production":
        # In production, only allow specific domains
        origins = os.getenv("CORS_ORIGINS", "").split(",")
        origins = [origin.strip() for origin in origins if origin.strip()]
        
        # Always allow the frontend domain
        frontend_url = os.getenv("FRONTEND_URL", "https://your-frontend-domain.com")
        if frontend_url not in origins:
            origins.append(frontend_url)
            
        return origins
    else:
        # In development, allow all origins
        return ["*"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
DAILY_QUOTA = int(os.getenv("DAILY_QUOTA", "10000"))

# Billing
DEFAULT_CREDITS = float(os.getenv("DEFAULT_CREDITS", "10.0"))
MIN_CREDITS_FOR_REQUEST = float(os.getenv("MIN_CREDITS_FOR_REQUEST", "0.001"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# Validation
def validate_config():
    """Validate that all required configuration is present"""
    required_vars = {
        "SECRET_KEY": SECRET_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
    }
    
    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value or var_value == "your-secret-key-change-in-production":
            missing_vars.append(var_name)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True 
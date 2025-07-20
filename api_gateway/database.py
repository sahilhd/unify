"""
Database configuration and models for UniLLM Phase 2
"""

from sqlalchemy import create_engine, Column, String, Integer, DateTime, DECIMAL, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./unillm.db")

# Handle PostgreSQL URL format for Railway
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine with optimized settings for production
if DATABASE_URL.startswith("postgresql://"):
    # PostgreSQL production settings
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False  # Set to True for SQL debugging
    )
else:
    # SQLite for local development
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

class User(Base):
    """User model for authentication and billing"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    api_key = Column(String, unique=True, index=True, nullable=False)
    credits = Column(DECIMAL(10, 4), default=0.0, nullable=False)
    rate_limit_per_minute = Column(Integer, default=60, nullable=False)
    daily_quota = Column(Integer, default=10000, nullable=False)  # tokens per day
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class UsageLog(Base):
    """Usage tracking for billing and analytics"""
    __tablename__ = "usage_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    model = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    tokens_used = Column(Integer, nullable=False)
    cost = Column(DECIMAL(10, 6), nullable=False)
    request_timestamp = Column(DateTime, default=func.now(), nullable=False)
    response_time_ms = Column(Integer, nullable=True)
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)

class BillingHistory(Base):
    """Billing transactions and credit purchases"""
    __tablename__ = "billing_history"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    amount = Column(DECIMAL(10, 4), nullable=False)
    description = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)  # 'credit_purchase', 'usage_charge', 'refund'
    stripe_payment_intent_id = Column(String, nullable=True, index=True)
    stripe_refund_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cost calculation constants
PROVIDER_COSTS = {
    "openai": {
        "gpt-3.5-turbo": 0.002,  # per 1K tokens
        "gpt-4": 0.03,
        "gpt-4-turbo": 0.03,
    },
    "anthropic": {
        "claude-3-sonnet": 0.015,
        "claude-3-haiku": 0.0025,
        "claude-3-opus": 0.075,
    },
    "gemini": {
        "gemini-pro": 0.001,
        "gemini-pro-vision": 0.001,
    },
    "mistral": {
        "mistral-small": 0.007,
        "mistral-medium": 0.014,
        "mistral-large": 0.056,
    },
    "cohere": {
        "command": 0.015,
        "command-light": 0.003,
    }
}

def calculate_cost(provider: str, model: str, tokens: int) -> float:
    """Calculate cost for a request"""
    base_cost = PROVIDER_COSTS.get(provider, {}).get(model, 0.01)  # default cost
    cost_per_1k = base_cost * 1.2  # 20% markup
    return (tokens / 1000) * cost_per_1k 
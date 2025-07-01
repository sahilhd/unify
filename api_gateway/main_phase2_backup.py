"""
UniLLM Phase 2: Enhanced API Gateway with Authentication and Billing
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
import json
import os
from dotenv import load_dotenv
from decimal import Decimal
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Import our modules
from database import get_db, User, UsageLog, BillingHistory, create_tables, calculate_cost
from auth import (
    get_password_hash, generate_api_key, authenticate_user, 
    create_access_token, get_current_user_api_key, get_current_user_jwt,
    require_admin
)
from middleware import RateLimitMiddleware, UsageTrackingMiddleware, CreditCheckMiddleware

# Import the custom Phase 2 LLM client
from phase2_llm_client import Phase2LLMClient

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="UniLLM API Gateway",
    description="Unified LLM API with authentication and billing",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(CreditCheckMiddleware)
# app.add_middleware(UsageTrackingMiddleware)  # Temporarily disabled due to hanging issues
app.add_middleware(RateLimitMiddleware)

# Initialize custom Phase 2 LLM client
llm_client = Phase2LLMClient()

# Create database tables
create_tables()

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    api_key: str
    credits: float
    rate_limit_per_minute: int
    daily_quota: int
    is_active: bool
    created_at: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    response: str
    tokens: int
    provider: str
    cost: float
    remaining_credits: float

class CreditPurchase(BaseModel):
    amount: float
    payment_method: str

class UsageStats(BaseModel):
    total_requests: int
    total_tokens: int
    total_cost: float
    requests_today: int
    tokens_today: int
    cost_today: float

# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db=Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    api_key = generate_api_key()
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        api_key=api_key,
        credits=10.0,  # Give 10 credits for free
        rate_limit_per_minute=60,
        daily_quota=10000
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        api_key=new_user.api_key,
        credits=float(new_user.credits),
        rate_limit_per_minute=new_user.rate_limit_per_minute,
        daily_quota=new_user.daily_quota,
        is_active=new_user.is_active,
        created_at=new_user.created_at.isoformat()
    )

@app.post("/auth/login")
async def login_user(user_data: UserLogin, db=Depends(get_db)):
    """Login user and return JWT token"""
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "credits": float(user.credits),
            "api_key": user.api_key
        }
    }

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user_jwt)):
    """Get current user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        api_key=current_user.api_key,
        credits=float(current_user.credits),
        rate_limit_per_minute=current_user.rate_limit_per_minute,
        daily_quota=current_user.daily_quota,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )

# Chat completion endpoint (enhanced)
@app.post("/chat/completions", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    current_user: User = Depends(get_current_user_api_key),
    db=Depends(get_db)
):
    """Enhanced chat completion with billing"""
    start_time = time.time()
    
    try:
        # Call the LLM
        response = llm_client.chat(
            model=request.model,
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )
        
        # Calculate response time
        response_time = int((time.time() - start_time) * 1000)
        
        # Estimate tokens (rough calculation)
        total_chars = sum(len(msg.get("content", "")) for msg in request.messages)
        estimated_tokens = max(total_chars // 4, 1)
        
        # Calculate cost - response is a ChatResponse object, not a dict
        provider = response.provider
        cost = calculate_cost(provider, request.model, estimated_tokens)
        
        # Update user credits - convert cost to Decimal to match user.credits type
        current_user.credits -= Decimal(str(cost))
        db.commit()
        
        return ChatResponse(
            response=response.content,
            tokens=estimated_tokens,
            provider=provider,
            cost=cost,
            remaining_credits=float(current_user.credits)
        )
        
    except Exception as e:
        # Log error
        usage_log = UsageLog(
            user_id=current_user.id,
            model=request.model,
            provider="unknown",
            tokens_used=0,
            cost=0,
            response_time_ms=int((time.time() - start_time) * 1000),
            success=False,
            error_message=str(e)
        )
        db.add(usage_log)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM request failed: {str(e)}"
        )

# Billing endpoints
@app.post("/billing/purchase-credits")
async def purchase_credits(
    purchase: CreditPurchase,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Purchase credits (accepts either JWT or API key)"""
    token = credentials.credentials
    # Try JWT first, then API key
    try:
        if is_jwt(token):
            current_user = get_current_user_jwt(credentials, db)
        else:
            current_user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Add credits to user account (convert float to Decimal)
    current_user.credits += Decimal(str(purchase.amount))
    
    # Log billing transaction
    billing_record = BillingHistory(
        user_id=current_user.id,
        amount=purchase.amount,
        description=f"Credit purchase via {purchase.payment_method}",
        transaction_type="credit_purchase"
    )
    
    db.add(billing_record)
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Credits purchased successfully",
        "credits_added": purchase.amount,
        "new_balance": float(current_user.credits)
    }

def is_jwt(token: str) -> bool:
    """Check if the token is a JWT (contains two dots)"""
    return token.count('.') == 2

@app.get("/billing/usage", response_model=UsageStats)
async def get_usage_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    token = credentials.credentials
    # Try JWT first, then API key
    try:
        if is_jwt(token):
            user = get_current_user_jwt(credentials, db)
        else:
            user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    from datetime import datetime, timedelta
    # Get all-time stats
    all_time = db.query(UsageLog).filter(UsageLog.user_id == user.id).all()
    total_requests = len(all_time)
    total_tokens = sum(log.tokens_used for log in all_time)
    total_cost = sum(float(log.cost) for log in all_time)
    # Get today's stats
    today = datetime.now().date()
    today_logs = db.query(UsageLog).filter(
        UsageLog.user_id == user.id,
        UsageLog.request_timestamp >= today
    ).all()
    requests_today = len(today_logs)
    tokens_today = sum(log.tokens_used for log in today_logs)
    cost_today = sum(float(log.cost) for log in today_logs)
    return UsageStats(
        total_requests=total_requests,
        total_tokens=total_tokens,
        total_cost=total_cost,
        requests_today=requests_today,
        tokens_today=tokens_today,
        cost_today=cost_today
    )

@app.get("/billing/history")
async def get_billing_history(
    current_user: User = Depends(get_current_user_jwt),
    db=Depends(get_db)
):
    """Get billing history"""
    history = db.query(BillingHistory).filter(
        BillingHistory.user_id == current_user.id
    ).order_by(BillingHistory.created_at.desc()).all()
    
    return [
        {
            "id": record.id,
            "amount": float(record.amount),
            "description": record.description,
            "transaction_type": record.transaction_type,
            "created_at": record.created_at.isoformat()
        }
        for record in history
    ]

# Admin endpoints
@app.get("/admin/users")
async def get_all_users(
    admin: User = Depends(require_admin),
    db=Depends(get_db)
):
    """Get all users (admin only)"""
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "credits": float(user.credits),
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]

@app.get("/admin/stats")
async def get_admin_stats(
    admin: User = Depends(require_admin),
    db=Depends(get_db)
):
    """Get platform statistics (admin only)"""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_usage = db.query(UsageLog).count()
    total_revenue = db.query(BillingHistory).filter(
        BillingHistory.transaction_type == "credit_purchase"
    ).with_entities(db.func.sum(BillingHistory.amount)).scalar() or 0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_requests": total_usage,
        "total_revenue": float(total_revenue)
    }

# Existing endpoints (enhanced)
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0",
        "features": ["authentication", "billing", "rate_limiting"]
    }

@app.get("/models")
async def list_models():
    """List available models"""
    return {
        "models": [
            {"id": "gpt-3.5-turbo", "provider": "openai", "cost_per_1k": 0.0024},
            {"id": "gpt-4", "provider": "openai", "cost_per_1k": 0.036},
            {"id": "claude-3-sonnet", "provider": "anthropic", "cost_per_1k": 0.018},
            {"id": "gemini-pro", "provider": "gemini", "cost_per_1k": 0.0012},
            {"id": "mistral-small", "provider": "mistral", "cost_per_1k": 0.0084},
        ]
    }

security = HTTPBearer()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
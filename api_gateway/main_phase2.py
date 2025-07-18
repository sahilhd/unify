"""
UniLLM Phase 2: Enhanced API Gateway with Authentication and Billing
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from datetime import datetime, timedelta
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
import re
import traceback
from unillm.exceptions import ModelNotFoundError
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request as StarletteRequest
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import logging
logger = logging.getLogger("uvicorn.error")

security = HTTPBearer()

# Import our modules
from database import get_db, User, UsageLog, BillingHistory, create_tables, calculate_cost
from auth import (
    get_password_hash, generate_api_key, authenticate_user, 
    create_access_token, get_current_user_api_key, get_current_user_jwt,
    require_admin, verify_token, get_user_by_api_key
)
from middleware import RateLimitMiddleware, UsageTrackingMiddleware, CreditCheckMiddleware
from payment_processor import PaymentProcessor, WebhookHandler

# Import the custom Phase 2 LLM client
from phase2_llm_client import Phase2LLMClient

# Import configuration
from config import (
    get_cors_origins, validate_config, ENVIRONMENT, DEBUG,
    DEFAULT_CREDITS, RATE_LIMIT_PER_MINUTE, DAILY_QUOTA
)

load_dotenv()

# Validate configuration on startup
try:
    validate_config()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please set the required environment variables before starting the server.")
    exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="UniLLM API Gateway",
    description="Unified LLM API with authentication and billing",
    version="2.0.0",
    debug=DEBUG
)

# Add SessionMiddleware for OAuth support
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "super-secret-session-key"),
    same_site="none",
    https_only=True
)

# Add CORS middleware with environment-specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
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

# Debug: Check if we reach OAuth configuration
logger.info("[STARTUP] About to configure OAuth")

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

class PaymentIntentRequest(BaseModel):
    credit_amount: int

class PaymentConfirmRequest(BaseModel):
    payment_intent_id: str

class UsageStats(BaseModel):
    total_requests: int
    total_tokens: int
    total_cost: float
    requests_today: int
    tokens_today: int
    cost_today: float

def is_jwt(token: str) -> bool:
    """Check if a token is a JWT token"""
    # JWT tokens have 3 parts separated by dots
    if not token or '.' not in token:
        return False
    
    parts = token.split('.')
    if len(parts) != 3:
        return False
    
    # Check if parts look like base64 (JWT format)
    try:
        import base64
        # Try to decode the header part
        base64.b64decode(parts[0] + '=' * (-len(parts[0]) % 4))
        return True
    except:
        return False

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
        credits=DEFAULT_CREDITS,  # Use config value
        rate_limit_per_minute=RATE_LIMIT_PER_MINUTE,
        daily_quota=DAILY_QUOTA
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
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Get current user information (accepts either JWT or API key)"""
    token = credentials.credentials
    
    # Try JWT first, then API key
    try:
        if is_jwt(token):
            # Try JWT authentication
            email = verify_token(token)
            if email:
                user = db.query(User).filter(User.email == email).first()
                if user and user.is_active:
                    return UserResponse(
                        id=user.id,
                        email=user.email,
                        api_key=user.api_key,
                        credits=float(user.credits),
                        rate_limit_per_minute=user.rate_limit_per_minute,
                        daily_quota=user.daily_quota,
                        is_active=user.is_active,
                        created_at=user.created_at.isoformat()
                    )
        
        # Try API key authentication
        user = get_user_by_api_key(db, token)
        if user and user.is_active:
            return UserResponse(
                id=user.id,
                email=user.email,
                api_key=user.api_key,
                credits=float(user.credits),
                rate_limit_per_minute=user.rate_limit_per_minute,
                daily_quota=user.daily_quota,
                is_active=user.is_active,
                created_at=user.created_at.isoformat()
            )
    except Exception as e:
        print(f"Auth error: {e}")
    
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Chat completion endpoint (enhanced)
@app.post("/chat/completions", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    current_user: User = Depends(get_current_user_api_key),
    db=Depends(get_db)
):
    """Enhanced chat completion with billing"""
    import sys
    start_time = time.time()
    print("\n[UniLLM] Incoming /chat/completions request:")
    print(json.dumps(request.dict(), indent=2, default=str))
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
        
        # Log successful usage
        usage_log = UsageLog(
            user_id=current_user.id,
            model=request.model,
            provider=provider,
            tokens_used=estimated_tokens,
            cost=cost,
            response_time_ms=response_time,
            success=True,
            error_message=None
        )
        db.add(usage_log)
        db.commit()
        
        return ChatResponse(
            response=response.content,
            tokens=estimated_tokens,
            provider=provider,
            cost=cost,
            remaining_credits=float(current_user.credits)
        )
    except ModelNotFoundError as e:
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
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[UniLLM] Exception in /chat/completions: {e}\n{tb}", file=sys.stderr)
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
            detail=f"LLM request failed: {str(e)}\nTraceback:\n{tb}"
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

@app.get("/billing/usage-over-time")
async def usage_over_time(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
    days: int = 30
):
    """Return daily usage stats for the current user for the last N days (default 30)."""
    token = credentials.credentials
    # Try JWT first, then API key
    try:
        if is_jwt(token):
            user = get_current_user_jwt(credentials, db)
        else:
            user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)

    # Query usage logs for the user in the date range
    logs = db.query(UsageLog).filter(
        UsageLog.user_id == user.id,
        UsageLog.request_timestamp >= start_date
    ).all()

    # Group by day
    usage_by_day = {}
    for log in logs:
        day = log.request_timestamp.date().isoformat()
        if day not in usage_by_day:
            usage_by_day[day] = {"requests": 0, "tokens": 0, "cost": 0.0}
        usage_by_day[day]["requests"] += 1
        usage_by_day[day]["tokens"] += log.tokens_used
        usage_by_day[day]["cost"] += float(log.cost)

    # Fill in days with zero usage
    result = []
    for i in range(days):
        day = (start_date + timedelta(days=i)).isoformat()
        stats = usage_by_day.get(day, {"requests": 0, "tokens": 0, "cost": 0.0})
        result.append({"date": day, **stats})

    return result

@app.get("/billing/history")
async def get_billing_history(
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

    history = db.query(BillingHistory).filter(
        BillingHistory.user_id == user.id
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

# Payment Processing Endpoints
@app.post("/billing/create-payment-intent")
async def create_payment_intent(
    request: PaymentIntentRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Create a Stripe payment intent for credit purchase"""
    token = credentials.credentials
    
    # Get current user
    try:
        if is_jwt(token):
            current_user = get_current_user_jwt(credentials, db)
        else:
            current_user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Create payment intent
    payment_data = PaymentProcessor.create_payment_intent(current_user, request.credit_amount)
    
    return {
        "client_secret": payment_data["client_secret"],
        "payment_intent_id": payment_data["payment_intent_id"],
        "amount_usd": payment_data["amount_usd"],
        "credit_amount": payment_data["credit_amount"]
    }

@app.post("/billing/confirm-payment")
async def confirm_payment(
    request: PaymentConfirmRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Confirm payment and add credits to user account"""
    token = credentials.credentials
    
    # Get current user
    try:
        if is_jwt(token):
            current_user = get_current_user_jwt(credentials, db)
        else:
            current_user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Process payment success
    result = PaymentProcessor.process_payment_success(db, request.payment_intent_id)
    
    return result

@app.get("/billing/credit-packages")
async def get_credit_packages():
    """Get available credit packages with pricing"""
    return PaymentProcessor.get_credit_packages()

@app.post("/billing/webhook")
async def stripe_webhook(request: Request, db=Depends(get_db)):
    """Handle Stripe webhook events"""
    payload = await request.body()
    signature = request.headers.get("stripe-signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")
    
    try:
        result = WebhookHandler.handle_webhook(payload, signature, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/billing/refund")
async def refund_payment(
    payment_intent_id: str,
    reason: str = "Customer request",
    admin: User = Depends(require_admin),
    db=Depends(get_db)
):
    """Process refund for a payment (admin only)"""
    result = PaymentProcessor.refund_payment(db, payment_intent_id, reason)
    return result

# Simple credit purchase endpoint (for testing)
@app.post("/billing/add-credits")
async def add_credits_direct(
    request: CreditPurchase,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Add credits directly (for testing purposes)"""
    token = credentials.credentials
    
    # Get current user
    try:
        if is_jwt(token):
            current_user = get_current_user_jwt(credentials, db)
        else:
            current_user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Add credits to user account (convert float to Decimal)
    current_user.credits += Decimal(str(request.amount))
    
    # Log billing transaction
    billing_record = BillingHistory(
        user_id=current_user.id,
        amount=request.amount,
        description=f"Credit purchase via {request.payment_method}",
        transaction_type="credit_purchase"
    )
    
    db.add(billing_record)
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Credits added successfully",
        "credits_added": request.amount,
        "new_balance": float(current_user.credits)
    }

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
    from unillm.registry import model_registry
    
    models = []
    for model in model_registry.list_models():
        provider = model_registry.get_provider(model)
        # Get cost from database or use default
        cost_per_1k = 0.01  # default cost
        if provider == "openai":
            if "gpt-4" in model:
                cost_per_1k = 0.036
            elif "gpt-3.5" in model:
                cost_per_1k = 0.0024
        elif provider == "anthropic":
            if "opus" in model:
                cost_per_1k = 0.075
            elif "sonnet" in model:
                cost_per_1k = 0.018
            elif "haiku" in model:
                cost_per_1k = 0.0025
        elif provider == "gemini":
            cost_per_1k = 0.0012
        elif provider == "mistral":
            if "large" in model:
                cost_per_1k = 0.056
            elif "medium" in model:
                cost_per_1k = 0.014
            elif "small" in model:
                cost_per_1k = 0.007
        
        models.append({
            "id": model,
            "provider": provider,
            "cost_per_1k": cost_per_1k
        })
    
    return {"models": models}

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

logger.info(f"[Google OAuth] Client ID: {GOOGLE_CLIENT_ID[:10]}..." if GOOGLE_CLIENT_ID else "NOT SET")
logger.info(f"[Google OAuth] Client Secret: {'SET' if GOOGLE_CLIENT_SECRET else 'NOT SET'}")

# Set up Authlib OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    },
)

logger.info("[Google OAuth] OAuth configuration completed")

@app.get("/auth/google/login")
async def google_login(request: StarletteRequest):
    logger.info("[Google OAuth] Login endpoint hit")
    # Hardcode the redirect_uri to match Google Cloud Console
    redirect_uri = "https://web-production-70deb.up.railway.app/auth/google/callback"
    logger.info(f"[Google OAuth] Using redirect_uri: {redirect_uri}")
    try:
        response = await oauth.google.authorize_redirect(request, redirect_uri)
        logger.info(f"[Google OAuth] Redirect response: {response}")
        return response
    except Exception as e:
        logger.info(f"[Google OAuth] Login exception: {e}")
        raise

@app.get("/auth/google/callback")
async def google_callback(request: StarletteRequest, db=Depends(get_db)):
    logger.info("[Google OAuth] Callback endpoint hit")
    logger.info(f"[Google OAuth] Request URL: {request.url}")
    logger.info(f"[Google OAuth] Request headers: {dict(request.headers)}")
    try:
        token = await oauth.google.authorize_access_token(request)
        logger.info(f"[Google OAuth] Token received: {token}")
        logger.info(f"[Google OAuth] Token type: {type(token)}, keys: {list(token.keys())}")
        user_info = token.get('userinfo')
        if not user_info:
            logger.info(f"[Google OAuth] userinfo missing from token: {token}")
            raise HTTPException(status_code=400, detail="Google login failed: userinfo missing")
        logger.info(f"[Google OAuth] user_info: {user_info}")
        email = user_info.get('email')
        if not email:
            logger.info("[Google OAuth] No email in user_info")
            raise HTTPException(status_code=400, detail="Google login failed: no email")
        # Find or create user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.info(f"[Google OAuth] Creating new user for email: {email}")
            api_key = generate_api_key()
            user = User(
                email=email,
                password_hash='',
                api_key=api_key,
                credits=DEFAULT_CREDITS,
                rate_limit_per_minute=RATE_LIMIT_PER_MINUTE,
                daily_quota=DAILY_QUOTA,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            logger.info(f"[Google OAuth] Found existing user for email: {email}")
        # Issue JWT token
        access_token = create_access_token(data={"sub": user.email})
        logger.info(f"[Google OAuth] Issued access_token: {access_token}")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        redirect_url = f"{frontend_url}/login-success?token={access_token}&api_key={user.api_key}"
        logger.info(f"[Google OAuth] Redirecting to: {redirect_url}")
        return RedirectResponse(redirect_url)
    except Exception as e:
        logger.info(f"[Google OAuth] Exception: {e}")
        raise

@app.get("/test")
async def test():
    logger.info("Test endpoint hit")
    return {"status": "ok"}

# API Key Management endpoints
class ApiKeyCreate(BaseModel):
    name: str

class ApiKeyResponse(BaseModel):
    id: str
    name: str
    key: str
    created_at: str
    last_used: Optional[str] = None
    is_active: bool

@app.get("/api-keys", response_model=List[ApiKeyResponse])
async def get_api_keys(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Get all API keys for the current user"""
    token = credentials.credentials
    
    # Get current user
    try:
        if is_jwt(token):
            current_user = get_current_user_jwt(credentials, db)
        else:
            current_user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # For now, return the user's main API key as a single key
    # In the future, this could be extended to support multiple API keys per user
    return [ApiKeyResponse(
        id="1",
        name="Primary API Key",
        key=current_user.api_key,
        created_at=current_user.created_at.isoformat(),
        last_used=None,  # Could be tracked in the future
        is_active=current_user.is_active
    )]

@app.post("/api-keys", response_model=ApiKeyResponse)
async def create_api_key(
    key_data: ApiKeyCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Create a new API key for the current user"""
    token = credentials.credentials
    
    # Get current user
    try:
        if is_jwt(token):
            current_user = get_current_user_jwt(credentials, db)
        else:
            current_user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Generate new API key
    new_api_key = generate_api_key()
    
    # Update user's API key (for now, we only support one key per user)
    # In the future, this could be extended to support multiple keys
    current_user.api_key = new_api_key
    db.commit()
    db.refresh(current_user)
    
    return ApiKeyResponse(
        id="1",
        name=key_data.name,
        key=new_api_key,
        created_at=current_user.updated_at.isoformat(),
        last_used=None,
        is_active=current_user.is_active
    )

@app.delete("/api-keys/{key_id}")
async def delete_api_key(
    key_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Delete an API key (currently only supports the primary key)"""
    token = credentials.credentials
    
    # Get current user
    try:
        if is_jwt(token):
            current_user = get_current_user_jwt(credentials, db)
        else:
            current_user = get_current_user_api_key(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # For now, we only support one API key per user
    # In the future, this could be extended to support multiple keys
    if key_id == "1":
        # Generate a new API key to replace the current one
        new_api_key = generate_api_key()
        current_user.api_key = new_api_key
        db.commit()
        return {"message": "API key regenerated successfully"}
    else:
        raise HTTPException(status_code=404, detail="API key not found")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
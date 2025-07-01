"""
Middleware for rate limiting, usage tracking, and request processing
"""

import time
import redis
from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import json
from database import get_db, UsageLog, User, calculate_cost
from auth import get_user_by_api_key
import os
from dotenv import load_dotenv

load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class RateLimitMiddleware:
    """Rate limiting middleware"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        
        # Skip rate limiting for health checks
        if request.url.path == "/health":
            await self.app(scope, receive, send)
            return
        
        # Get API key from header
        api_key = request.headers.get("authorization", "")
        if api_key.startswith("Bearer "):
            api_key = api_key[7:]
        
        if not api_key:
            await self.app(scope, receive, send)
            return
        
        # Check rate limit
        if not self._check_rate_limit(api_key):
            response = JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded"}
            )
            await response(scope, receive, send)
            return
        
        await self.app(scope, receive, send)
    
    def _check_rate_limit(self, api_key: str) -> bool:
        """Check if request is within rate limit"""
        key = f"rate_limit:{api_key}"
        current = redis_client.get(key)
        
        if current is None:
            redis_client.setex(key, 60, 1)  # 1 minute window
            return True
        
        current_count = int(current)
        if current_count >= 60:  # Default 60 requests per minute
            return False
        
        redis_client.incr(key)
        return True

class UsageTrackingMiddleware:
    """Usage tracking middleware"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        start_time = time.time()
        
        # Create a custom response handler
        async def response_handler(response: Response):
            # Calculate response time
            response_time = int((time.time() - start_time) * 1000)
            
            # Track usage for chat completions
            if request.url.path == "/chat/completions" and response.status_code == 200:
                await self._track_usage(request, response, response_time)
        
        # Override the send function to capture response
        original_send = send
        
        async def custom_send(message):
            if message["type"] == "http.response.start":
                # Store response info for tracking
                scope["response_status"] = message["status"]
            elif message["type"] == "http.response.body":
                # Track usage after response is complete
                if scope.get("response_status") == 200:
                    await self._track_usage(request, None, int((time.time() - start_time) * 1000))
            
            await original_send(message)
        
        await self.app(scope, receive, custom_send)
    
    async def _track_usage(self, request: Request, response: Optional[Response], response_time: int):
        """Track usage in database"""
        try:
            # Get API key
            api_key = request.headers.get("authorization", "")
            if api_key.startswith("Bearer "):
                api_key = api_key[7:]
            
            if not api_key:
                return
            
            # Get user from database
            db = next(get_db())
            user = get_user_by_api_key(db, api_key)
            if not user:
                return
            
            # Parse request body to get model info
            body = await request.body()
            if body:
                try:
                    data = json.loads(body)
                    model = data.get("model", "unknown")
                    provider = self._get_provider_from_model(model)
                    
                    # Estimate tokens (this is a rough estimate)
                    messages = data.get("messages", [])
                    estimated_tokens = self._estimate_tokens(messages)
                    
                    # Calculate cost
                    cost = calculate_cost(provider, model, estimated_tokens)
                    
                    # Log usage
                    usage_log = UsageLog(
                        user_id=user.id,
                        model=model,
                        provider=provider,
                        tokens_used=estimated_tokens,
                        cost=cost,
                        response_time_ms=response_time,
                        success=True
                    )
                    
                    db.add(usage_log)
                    
                    # Deduct credits
                    user.credits -= cost
                    
                    db.commit()
                    
                except (json.JSONDecodeError, Exception) as e:
                    # Log error
                    usage_log = UsageLog(
                        user_id=user.id,
                        model="unknown",
                        provider="unknown",
                        tokens_used=0,
                        cost=0,
                        response_time_ms=response_time,
                        success=False,
                        error_message=str(e)
                    )
                    db.add(usage_log)
                    db.commit()
            
        except Exception as e:
            # Log error but don't fail the request
            print(f"Usage tracking error: {e}")
    
    def _get_provider_from_model(self, model: str) -> str:
        """Get provider from model name"""
        if model.startswith("gpt-"):
            return "openai"
        elif model.startswith("claude-"):
            return "anthropic"
        elif model.startswith("gemini-"):
            return "gemini"
        elif model.startswith("mistral-"):
            return "mistral"
        elif model.startswith("command"):
            return "cohere"
        else:
            return "unknown"
    
    def _estimate_tokens(self, messages: list) -> int:
        """Rough token estimation"""
        total_tokens = 0
        for message in messages:
            content = message.get("content", "")
            # Rough estimate: 1 token ≈ 4 characters
            total_tokens += len(content) // 4
        return max(total_tokens, 1)  # Minimum 1 token

class CreditCheckMiddleware:
    """Check user credits before processing request"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        
        # Skip credit check for non-chat endpoints
        if request.url.path != "/chat/completions":
            await self.app(scope, receive, send)
            return
        
        # Get API key
        api_key = request.headers.get("authorization", "")
        if api_key.startswith("Bearer "):
            api_key = api_key[7:]
        
        if not api_key:
            await self.app(scope, receive, send)
            return
        
        # Check credits
        db = next(get_db())
        user = get_user_by_api_key(db, api_key)
        
        if user and user.credits <= 0:
            response = JSONResponse(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                content={"detail": "Insufficient credits. Please add credits to continue."}
            )
            await response(scope, receive, send)
            return
        
        await self.app(scope, receive, send) 
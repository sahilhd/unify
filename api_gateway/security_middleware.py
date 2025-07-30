"""
Security middleware for UniLLM API Gateway
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
from config import ENVIRONMENT

class SecurityHeadersMiddleware:
    """Add security headers to all responses"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                
                # Add security headers
                security_headers = [
                    # Prevent clickjacking
                    (b"x-frame-options", b"DENY"),
                    # Prevent MIME type sniffing
                    (b"x-content-type-options", b"nosniff"),
                    # XSS protection
                    (b"x-xss-protection", b"1; mode=block"),
                    # Referrer policy
                    (b"referrer-policy", b"strict-origin-when-cross-origin"),
                    # Remove server header for security obscurity
                    (b"server", b"UniLLM"),
                ]
                
                # Add HSTS header in production
                if ENVIRONMENT == "production":
                    security_headers.append(
                        (b"strict-transport-security", b"max-age=31536000; includeSubDomains")
                    )
                
                # Add Content Security Policy
                csp_policy = (
                    "default-src 'self'; "
                    "script-src 'self' 'unsafe-inline'; "
                    "style-src 'self' 'unsafe-inline'; "
                    "img-src 'self' data: https:; "
                    "connect-src 'self' https:; "
                    "font-src 'self'; "
                    "object-src 'none'; "
                    "media-src 'self'; "
                    "frame-src 'none';"
                )
                security_headers.append(
                    (b"content-security-policy", csp_policy.encode())
                )
                
                headers.extend(security_headers)
                message["headers"] = headers
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)

class RequestLoggingMiddleware:
    """Log requests for security monitoring"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        start_time = time.time()
        
        # Log request details (for security monitoring)
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent", "")
        method = request.method
        path = request.url.path
        
        # Track failed authentication attempts
        failed_auth = False
        
        async def send_wrapper(message):
            nonlocal failed_auth
            if message["type"] == "http.response.start":
                status_code = message["status"]
                if status_code == 401:
                    failed_auth = True
                    print(f"⚠️  SECURITY: Failed auth attempt from {ip_address} to {method} {path} - UA: {user_agent[:100]}")
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
        
        # Log suspicious activity
        process_time = time.time() - start_time
        if process_time > 10:  # Slow requests might indicate attacks
            print(f"⚠️  SECURITY: Slow request ({process_time:.2f}s) from {ip_address} to {method} {path}")

class BruteForceProtectionMiddleware:
    """Protect against brute force attacks"""
    
    def __init__(self, app):
        self.app = app
        self.failed_attempts = {}  # In production, use Redis
        self.max_attempts = 5
        self.lockout_time = 900  # 15 minutes
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        ip_address = request.client.host
        
        # Skip brute force protection for utility endpoints
        if request.url.path in ["/health", "/auth/check-password-strength", "/test"]:
            await self.app(scope, receive, send)
            return
        
        # Check if IP is locked out
        if self._is_locked_out(ip_address):
            response = JSONResponse(
                status_code=429,
                content={"detail": "Too many failed attempts. Please try again later."}
            )
            await response(scope, receive, send)
            return
        
        # Track failed login attempts
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                if status_code == 401 and request.url.path == "/auth/login":
                    self._record_failed_attempt(ip_address)
                elif status_code == 200 and request.url.path == "/auth/login":
                    self._clear_failed_attempts(ip_address)
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
    
    def _is_locked_out(self, ip_address: str) -> bool:
        """Check if IP address is locked out"""
        if ip_address not in self.failed_attempts:
            return False
        
        attempts, last_attempt = self.failed_attempts[ip_address]
        if time.time() - last_attempt > self.lockout_time:
            del self.failed_attempts[ip_address]
            return False
        
        return attempts >= self.max_attempts
    
    def _record_failed_attempt(self, ip_address: str):
        """Record a failed login attempt"""
        current_time = time.time()
        if ip_address in self.failed_attempts:
            attempts, _ = self.failed_attempts[ip_address]
            self.failed_attempts[ip_address] = (attempts + 1, current_time)
        else:
            self.failed_attempts[ip_address] = (1, current_time)
        
        print(f"⚠️  SECURITY: Failed login attempt #{self.failed_attempts[ip_address][0]} from {ip_address}")
    
    def _clear_failed_attempts(self, ip_address: str):
        """Clear failed attempts on successful login"""
        if ip_address in self.failed_attempts:
            del self.failed_attempts[ip_address] 
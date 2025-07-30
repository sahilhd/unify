"""
Authentication system for UniLLM Phase 2
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import secrets
import string
import re
from database import get_db, User

# Import configuration
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, MIN_PASSWORD_LENGTH, REQUIRE_PASSWORD_COMPLEXITY

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

def validate_password_strength(password: str) -> None:
    """Validate password meets security requirements"""
    if len(password) < MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
        )
    
    if REQUIRE_PASSWORD_COMPLEXITY:
        # Check for complexity requirements
        if not re.search(r"[A-Z]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter"
            )
        if not re.search(r"[a-z]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one lowercase letter"
            )
        if not re.search(r"\d", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one number"
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one special character"
            )

def check_password_strength(password: str) -> dict:
    """Check password strength and return detailed feedback"""
    result = {
        "is_valid": True,
        "score": 0,
        "requirements": {},
        "suggestions": []
    }
    
    # Check length
    length_ok = len(password) >= MIN_PASSWORD_LENGTH
    result["requirements"]["length"] = {
        "met": length_ok,
        "required": MIN_PASSWORD_LENGTH,
        "current": len(password),
        "description": f"At least {MIN_PASSWORD_LENGTH} characters"
    }
    if length_ok:
        result["score"] += 20
    else:
        result["is_valid"] = False
        result["suggestions"].append(f"Add {MIN_PASSWORD_LENGTH - len(password)} more characters")
    
    if REQUIRE_PASSWORD_COMPLEXITY:
        # Check uppercase
        has_upper = bool(re.search(r"[A-Z]", password))
        result["requirements"]["uppercase"] = {
            "met": has_upper,
            "description": "At least one uppercase letter (A-Z)"
        }
        if has_upper:
            result["score"] += 20
        else:
            result["is_valid"] = False
            result["suggestions"].append("Add at least one uppercase letter")
        
        # Check lowercase
        has_lower = bool(re.search(r"[a-z]", password))
        result["requirements"]["lowercase"] = {
            "met": has_lower,
            "description": "At least one lowercase letter (a-z)"
        }
        if has_lower:
            result["score"] += 20
        else:
            result["is_valid"] = False
            result["suggestions"].append("Add at least one lowercase letter")
        
        # Check numbers
        has_number = bool(re.search(r"\d", password))
        result["requirements"]["number"] = {
            "met": has_number,
            "description": "At least one number (0-9)"
        }
        if has_number:
            result["score"] += 20
        else:
            result["is_valid"] = False
            result["suggestions"].append("Add at least one number")
        
        # Check special characters
        has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
        result["requirements"]["special"] = {
            "met": has_special,
            "description": "At least one special character (!@#$%^&*(),.?\":{}|<>)"
        }
        if has_special:
            result["score"] += 20
        else:
            result["is_valid"] = False
            result["suggestions"].append("Add at least one special character (!@#$%^&*(),.?\":{}|<>)")
    else:
        # If complexity not required, full score for basic length
        if length_ok:
            result["score"] = 100
    
    # Add strength description
    if result["score"] >= 100:
        result["strength"] = "Strong"
        result["strength_color"] = "green"
    elif result["score"] >= 80:
        result["strength"] = "Good"
        result["strength_color"] = "yellow"
    elif result["score"] >= 60:
        result["strength"] = "Fair"
        result["strength_color"] = "orange"
    else:
        result["strength"] = "Weak"
        result["strength_color"] = "red"
    
    return result

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def generate_api_key() -> str:
    """Generate a secure API key"""
    alphabet = string.ascii_letters + string.digits
    return "unillm_" + ''.join(secrets.choice(alphabet) for _ in range(32))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_api_key(db: Session, api_key: str) -> Optional[User]:
    """Get user by API key"""
    return db.query(User).filter(User.api_key == api_key).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_current_user_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from API key in Authorization header"""
    api_key = credentials.credentials
    
    # Check if it's a Bearer token format
    if api_key.startswith("Bearer "):
        api_key = api_key[7:]
    
    user = get_user_by_api_key(db, api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_user_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token"""
    token = credentials.credentials
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_admin(user: User = Depends(get_current_user_jwt)) -> User:
    """Require admin privileges"""
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user 
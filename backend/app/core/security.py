"""
Security module for password hashing and JWT token management.
Uses bcrypt for password hashing (cost >= 12) and PyJWT for token handling.
"""
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..models.user import User
from .config import settings
from .database import get_db

# HTTP Bearer token scheme
security_scheme = HTTPBearer()


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt with cost factor 12.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password as string (bcrypt hash includes salt)
    """
    # Use cost factor 12 per security requirements (REQ-SEC-001)
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash to check against
        
    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token with expiry claim.
    
    Args:
        data: Payload data to encode in token (should include 'sub' for user ID)
        expires_delta: Optional custom expiry duration
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    # Calculate expiry time
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    
    # Add exp claim (required per REQ-SEC-001)
    to_encode.update({"exp": expire})
    
    # Encode JWT using PyJWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to extract and verify the current authenticated user from JWT token.
    
    This is the primary authentication dependency used on protected routes.
    Enforces server-side authentication per REQ-AUTH-002.
    
    Args:
        credentials: HTTP Bearer credentials from request header
        db: Database session
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Decode token
    payload = decode_access_token(credentials.credentials)
    
    # Extract user ID from 'sub' claim (JWT standard)
    user_id_str: str | None = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: missing subject",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Convert string ID back to integer (JWT sub is string per spec)
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload: malformed user ID",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user


# Alias for require_auth to match architecture contract naming
require_auth = get_current_user

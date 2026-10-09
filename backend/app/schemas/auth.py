"""Authentication request and response schemas."""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    """Login request with email and password.
    
    Validates email format and password length constraints per LLD Section 4.4.
    """
    email: EmailStr = Field(..., description="User email address", max_length=255)
    password: str = Field(
        ..., 
        description="User password",
        min_length=8,
        max_length=128
    )

    @field_validator('password')
    @classmethod
    def validate_password_not_empty(cls, v: str) -> str:
        """Ensure password is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Password cannot be empty or whitespace only")
        return v


class UserSummary(BaseModel):
    """User summary for responses.
    
    Explicitly excludes password_hash and other sensitive fields.
    """
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")
    display_name: str = Field(..., description="User display name", alias="displayName")

    class Config:
        populate_by_name = True
        from_attributes = True


class AuthTokenPayload(BaseModel):
    """Authentication token payload."""
    token_type: str = Field("Bearer", description="Token type", alias="tokenType")
    access_token: str = Field(..., description="JWT access token", alias="accessToken")
    expires_at: datetime = Field(..., description="Token expiration timestamp", alias="expiresAt")

    class Config:
        populate_by_name = True


class AuthResponse(BaseModel):
    """Authentication response with user info and token.
    
    Response schema for POST /api/v1/auth/login per LLD Section 4.4.
    """
    user: UserSummary = Field(..., description="Authenticated user information")
    auth: AuthTokenPayload = Field(..., description="Authentication token payload")

"""Unit tests for auth_service.py."""
import pytest
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.services.auth_service import AuthService


class TestAuthService:
    """Test suite for AuthService."""
    
    def test_verify_credentials_success(self, test_db: Session, test_user: User):
        """Test successful credential verification."""
        service = AuthService(test_db)
        
        # Verify with correct password
        user = service.verify_credentials("test@example.com", "testpass123")
        
        assert user is not None
        assert user.id == test_user.id
        assert user.email == "test@example.com"
    
    def test_verify_credentials_wrong_password(self, test_db: Session, test_user: User):
        """Test credential verification with wrong password."""
        service = AuthService(test_db)
        
        # Attempt verification with wrong password
        with pytest.raises(HTTPException) as exc_info:
            service.verify_credentials("test@example.com", "wrongpassword")
        
        assert exc_info.value.status_code == 401
        assert "Email or password is incorrect" in exc_info.value.detail
    
    def test_verify_credentials_user_not_found(self, test_db: Session):
        """Test credential verification with non-existent user."""
        service = AuthService(test_db)
        
        # Attempt verification with non-existent email
        with pytest.raises(HTTPException) as exc_info:
            service.verify_credentials("nonexistent@example.com", "anypassword")
        
        assert exc_info.value.status_code == 401
        assert "Email or password is incorrect" in exc_info.value.detail
    
    def test_issue_token(self, test_db: Session, test_user: User):
        """Test JWT token issuance."""
        from datetime import UTC
        
        service = AuthService(test_db)
        
        # Issue token
        access_token, expires_at = service.issue_token(test_user)
        
        assert access_token is not None
        assert isinstance(access_token, str)
        assert len(access_token) > 0
        assert isinstance(expires_at, datetime)
        assert expires_at > datetime.now(UTC)
    
    def test_issue_token_contains_user_id(self, test_db: Session, test_user: User):
        """Test that issued token contains user ID in payload."""
        from app.core.security import decode_access_token
        
        service = AuthService(test_db)
        
        # Issue token
        access_token, _ = service.issue_token(test_user)
        
        # Decode and verify payload
        payload = decode_access_token(access_token)
        assert payload is not None
        assert "sub" in payload
        assert payload["sub"] == str(test_user.id)
    
    def test_sign_out(self, test_db: Session, test_user: User):
        """Test sign-out bookkeeping."""
        service = AuthService(test_db)
        
        # Sign out should complete without error
        service.sign_out(test_user)
        
        # No exception means success (JWT is stateless)
    
    def test_password_hashing_verification(self):
        """Test password hashing and verification."""
        plain_password = "mysecretpassword"
        
        # Hash password
        hashed = get_password_hash(plain_password)
        
        assert hashed is not None
        assert hashed != plain_password
        assert len(hashed) > 20  # bcrypt hashes are longer
        
        # Verify correct password
        assert verify_password(plain_password, hashed) is True
        
        # Verify wrong password
        assert verify_password("wrongpassword", hashed) is False
    
    def test_bcrypt_cost_factor(self):
        """Test that bcrypt uses cost factor 12."""
        password = "testpassword"
        hashed = get_password_hash(password)
        
        # bcrypt hash format: $2b$12$...
        # The '12' part indicates cost factor
        assert hashed.startswith("$2b$12$") or hashed.startswith("$2a$12$")

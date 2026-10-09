"""Authentication service for credential verification and token issuance."""
import logging
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import log_auth_event
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
        self.user_repo = UserRepository(db)
    
    def verify_credentials(self, email: str, password: str) -> User:
        """Verify learner credentials and return user.
        
        Args:
            email: User email address
            password: Plain text password
            
        Returns:
            User instance if credentials are valid
            
        Raises:
            HTTPException: 401 if credentials are invalid
        """
        # Fetch user by email
        user = self.user_repo.get_by_email(email)
        
        if not user:
            log_auth_event(
                logger,
                event_type="sign_in_failed",
                user_id=None,
                email=email,
                outcome="invalid_credentials",
                reason="user_not_found"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is incorrect."
            )
        
        # Verify password
        if not verify_password(password, user.password_hash):
            log_auth_event(
                logger,
                event_type="sign_in_failed",
                user_id=user.id,
                email=email,
                outcome="invalid_credentials",
                reason="password_mismatch"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is incorrect."
            )
        
        # Log successful auth
        log_auth_event(
            logger,
            event_type="sign_in_success",
            user_id=user.id,
            email=email,
            outcome="success"
        )
        
        return user
    
    def issue_token(self, user: User) -> tuple[str, datetime]:
        """Issue JWT access token for authenticated user.
        
        Args:
            user: Authenticated User instance
            
        Returns:
            Tuple of (access_token, expires_at)
        """
        # Create token payload with user ID as 'sub' claim
        token_data = {"sub": str(user.id)}
        
        # Calculate expiry
        expires_delta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        expires_at = datetime.now(UTC) + expires_delta
        
        # Create JWT token
        access_token = create_access_token(
            data=token_data,
            expires_delta=expires_delta
        )
        
        return access_token, expires_at
    
    def sign_out(self, user: User) -> None:
        """Handle sign-out bookkeeping.
        
        Args:
            user: User instance signing out
        """
        # Log sign-out event
        log_auth_event(
            logger=logger,
            event_type="sign_out",
            user_id=user.id,
            email=user.email,
            outcome="success"
        )
        
        # For JWT-based auth, token invalidation happens client-side
        # Server just logs the event
        # In session-based mode, this would clear the session

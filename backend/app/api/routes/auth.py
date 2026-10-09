"""Authentication routes for login and logout."""
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_auth
from app.core.database import get_db
from app.core.logging import get_logger, log_auth_event
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
logger = get_logger(__name__)


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def login(
    request: LoginRequest,
    db: Annotated[Session, Depends(get_db)]
) -> AuthResponse:
    """Authenticate learner and create authenticated session.
    
    Args:
        request: Login credentials (email and password)
        db: Database session
        
    Returns:
        AuthResponse with user info and access token
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    auth_service = AuthService(db)
    
    # Verify credentials
    user = auth_service.verify_credentials(request.email, request.password)
    
    # Issue token
    access_token, expires_at = auth_service.issue_token(user)
    
    # Build response
    return AuthResponse(
        user={
            "id": user.id,
            "email": user.email,
            "displayName": user.display_name
        },
        auth={
            "tokenType": "Bearer",
            "accessToken": access_token,
            "expiresAt": expires_at
        }
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    current_user: Annotated[User, Depends(require_auth)]
):
    """End authenticated session and clear session state.
    
    Args:
        current_user: Authenticated user from token
        
    Returns:
        204 No Content
    """
    # Log sign-out event
    log_auth_event(
        logger=logger,
        event_type="sign_out",
        user_id=current_user.id,
        email=current_user.email,
        outcome="success"
    )
    
    # JWT is stateless, so no server-side cleanup needed
    # Client will discard the token

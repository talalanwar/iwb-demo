"""
Structured logging setup for authentication, saves, and review actions.
Provides consistent logging without exposing sensitive data.
"""
import logging
import sys
from datetime import UTC, datetime
from typing import Any

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Logger name (typically __name__ from calling module)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_auth_event(
    logger: logging.Logger,
    event_type: str,
    user_id: int | None = None,
    email: str | None = None,
    outcome: str = "success",
    request_id: str | None = None,
    **extra_context: Any
) -> None:
    """
    Log an authentication event.
    
    Events include: sign-in success, sign-in failure, sign-out.
    Per REQ-SEC-003, passwords and full tokens are NEVER logged.
    
    Args:
        logger: Logger instance
        event_type: Type of auth event (e.g., "login", "logout", "token_verify")
        user_id: User ID if known
        email: User email (will be masked for privacy)
        outcome: Event outcome ("success" or "failure")
        request_id: Request ID for tracing
        extra_context: Additional context fields
    """
    # Mask email for privacy - show only first char and domain
    masked_email = None
    if email:
        parts = email.split('@')
        if len(parts) == 2:
            masked_email = f"{parts[0][0]}***@{parts[1]}"
        else:
            masked_email = "***"
    
    log_data = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": f"auth_{event_type}",
        "user_id": user_id,
        "email": masked_email,
        "outcome": outcome,
        "request_id": request_id,
        **extra_context
    }
    
    # Remove None values for cleaner logs
    log_data = {k: v for k, v in log_data.items() if v is not None}
    
    if outcome == "success":
        logger.info(f"Auth event: {event_type}", extra=log_data)
    else:
        logger.warning(f"Auth event failed: {event_type}", extra=log_data)


def log_save_event(
    logger: logging.Logger,
    resource_type: str,
    resource_id: str,
    user_id: int,
    operation: str = "update",
    request_id: str | None = None,
    **extra_context: Any
) -> None:
    """
    Log a workspace save operation.
    
    Events include: workspace save, story save, vision save.
    Per REQ-SEC-003, unsent drafts are NEVER logged.
    
    Args:
        logger: Logger instance
        resource_type: Type of resource (e.g., "workspace", "story", "vision")
        resource_id: ID of saved resource
        user_id: User who performed the save
        operation: Operation type ("create", "update", "delete")
        request_id: Request ID for tracing
        extra_context: Additional context fields
    """
    log_data = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": f"save_{resource_type}",
        "resource_type": resource_type,
        "resource_id": resource_id,
        "user_id": user_id,
        "operation": operation,
        "request_id": request_id,
        **extra_context
    }
    
    # Remove None values
    log_data = {k: v for k, v in log_data.items() if v is not None}
    
    logger.info(f"Save event: {resource_type} {operation}", extra=log_data)


def log_review_action(
    logger: logging.Logger,
    action_type: str,
    workspace_id: str,
    reviewer_name: str | None = None,
    user_id: int | None = None,
    request_id: str | None = None,
    **extra_context: Any
) -> None:
    """
    Log a review-related action.
    
    Events include: review access, review note creation, share token generation.
    Per REQ-SEC-003, note drafts before submission are NEVER logged.
    
    Args:
        logger: Logger instance
        action_type: Type of review action (e.g., "access", "note_create", "share_generate")
        workspace_id: Workspace being reviewed
        reviewer_name: Name of reviewer (for note creation)
        user_id: User ID if authenticated learner
        request_id: Request ID for tracing
        extra_context: Additional context fields
    """
    log_data = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": f"review_{action_type}",
        "workspace_id": workspace_id,
        "reviewer_name": reviewer_name,
        "user_id": user_id,
        "request_id": request_id,
        **extra_context
    }
    
    # Remove None values
    log_data = {k: v for k, v in log_data.items() if v is not None}
    
    logger.info(f"Review action: {action_type}", extra=log_data)


def log_authorization_failure(
    logger: logging.Logger,
    user_id: int | None,
    route: str,
    reason: str,
    request_id: str | None = None,
    **extra_context: Any
) -> None:
    """
    Log an authorization failure event.
    
    Per REQ-AUTH-002, authorization failures must be logged with
    request ID, user ID, route, and reason.
    
    Args:
        logger: Logger instance
        user_id: User ID if known (may be None for invalid tokens)
        route: Route that was accessed
        reason: Reason for authorization failure
        request_id: Request ID for tracing
        extra_context: Additional context fields
    """
    log_data = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": "authorization_failure",
        "user_id": user_id,
        "route": route,
        "reason": reason,
        "request_id": request_id,
        **extra_context
    }
    
    # Remove None values
    log_data = {k: v for k, v in log_data.items() if v is not None}
    
    logger.warning(f"Authorization failed: {reason}", extra=log_data)


# Create module-level logger
logger = get_logger(__name__)

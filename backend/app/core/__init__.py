"""
Core module containing configuration, security, logging, errors, and database utilities.
"""
from .config import settings
from .database import get_db, get_engine, get_session_factory, init_db
from .errors import (
    ApiError,
    ApiErrorResponse,
    create_error_response,
    register_exception_handlers,
)
from .logging import (
    get_logger,
    log_auth_event,
    log_authorization_failure,
    log_review_action,
    log_save_event,
)
from .security import (
    create_access_token,
    decode_access_token,
    get_current_user,
    get_password_hash,
    require_auth,
    verify_password,
)

__all__ = [
    "ApiError",
    "ApiErrorResponse",
    "create_access_token",
    "create_error_response",
    "decode_access_token",
    "get_current_user",
    "get_db",
    "get_engine",
    "get_logger",
    "get_password_hash",
    "get_session_factory",
    "init_db",
    "log_auth_event",
    "log_authorization_failure",
    "log_review_action",
    "log_save_event",
    "register_exception_handlers",
    "require_auth",
    "settings",
    "verify_password",
]

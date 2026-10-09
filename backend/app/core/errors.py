"""
Error handling module with standard API error envelope and exception handlers.
Provides consistent error responses across all endpoints.
"""
from typing import Any
from uuid import uuid4

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Individual error detail for field-level validation errors."""
    field: str
    issue: str


class ApiError(BaseModel):
    """
    Standard API error envelope.
    
    All error responses follow this structure for consistency.
    """
    code: str
    message: str
    details: list[ErrorDetail] = []
    requestId: str | None = None


class ApiErrorResponse(BaseModel):
    """Top-level error response wrapper."""
    error: ApiError


def create_error_response(
    code: str,
    message: str,
    details: list[ErrorDetail] | None = None,
    request_id: str | None = None
) -> ApiErrorResponse:
    """
    Create a standardized error response.
    
    Args:
        code: Error code constant (e.g., "AUTH_INVALID_CREDENTIALS")
        message: Human-readable error message
        details: Optional list of field-level error details
        request_id: Optional request ID for tracing
        
    Returns:
        Standardized API error response
    """
    if details is None:
        details = []
    if request_id is None:
        request_id = f"req_{uuid4().hex[:12]}"
    
    return ApiErrorResponse(
        error=ApiError(
            code=code,
            message=message,
            details=details,
            requestId=request_id
        )
    )


async def http_401_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle 401 Unauthorized errors.
    
    Returns consistent error format for authentication failures.
    """
    error = create_error_response(
        code="AUTH_REQUIRED",
        message="Authentication is required to access this resource",
        request_id=getattr(request.state, 'request_id', None)
    )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=error.model_dump(),
        headers={"WWW-Authenticate": "Bearer"}
    )


async def http_403_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle 403 Forbidden errors.
    
    Returns consistent error format for authorization failures.
    """
    error = create_error_response(
        code="AUTH_FORBIDDEN",
        message="You do not have permission to access this resource",
        request_id=getattr(request.state, 'request_id', None)
    )
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=error.model_dump()
    )


async def http_404_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle 404 Not Found errors.
    
    Returns consistent error format for missing resources.
    """
    error = create_error_response(
        code="RESOURCE_NOT_FOUND",
        message="The requested resource was not found",
        request_id=getattr(request.state, 'request_id', None)
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error.model_dump()
    )


async def http_422_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle 422 Unprocessable Entity errors (validation failures).
    
    Returns consistent error format for validation errors with field-level details.
    """
    # Extract validation errors if available from FastAPI RequestValidationError
    details = []
    if hasattr(exc, 'errors'):
        for error in exc.errors():
            field = '.'.join(str(loc) for loc in error.get('loc', []))
            details.append(ErrorDetail(
                field=field,
                issue=error.get('msg', 'Validation error')
            ))
    
    error = create_error_response(
        code="VALIDATION_ERROR",
        message="Request validation failed",
        details=details,
        request_id=getattr(request.state, 'request_id', None)
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error.model_dump()
    )


async def http_500_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle 500 Internal Server Error.
    
    Returns consistent error format for server errors without exposing internals.
    """
    # Log the actual exception internally (will be added in logging.py)
    error = create_error_response(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred. Please try again later.",
        request_id=getattr(request.state, 'request_id', None)
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error.model_dump()
    )


def register_exception_handlers(app: Any) -> None:
    """
    Register all exception handlers with the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(status.HTTP_401_UNAUTHORIZED, http_401_handler)
    app.add_exception_handler(status.HTTP_403_FORBIDDEN, http_403_handler)
    app.add_exception_handler(status.HTTP_404_NOT_FOUND, http_404_handler)
    app.add_exception_handler(status.HTTP_422_UNPROCESSABLE_ENTITY, http_422_handler)
    app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, http_500_handler)


# Aliases for consistency with main.py imports
handle_unauthorized_error = http_401_handler
handle_authorization_error = http_403_handler
handle_not_found_error = http_404_handler
handle_validation_error = http_422_handler
handle_server_error = http_500_handler

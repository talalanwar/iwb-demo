"""Common schema definitions for API error responses."""
from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Field-level validation error detail."""
    field: str | None = Field(None, description="Field name that caused the error")
    message: str = Field(..., description="Error message")
    value: Any | None = Field(None, description="Invalid value that was provided")


class ApiError(BaseModel):
    """Standard API error envelope.
    
    Used for all error responses across the API to ensure consistent
    error handling on the client side.
    """
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: list[ErrorDetail] = Field(default_factory=list, description="Field-level error details")
    request_id: str | None = Field(None, description="Request ID for tracking", alias="requestId")

    class Config:
        populate_by_name = True  # Allow both snake_case and camelCase

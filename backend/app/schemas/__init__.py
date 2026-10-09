"""Pydantic schemas package for API contracts.

This package contains request/response schemas matching LLD Section 4 and 5.1.
All schemas use Field validators for string lengths, required fields, and array bounds.
Response schemas explicitly exclude password_hash, tokens, and sensitive fields.
"""
from .auth import (
    AuthResponse,
    AuthTokenPayload,
    LoginRequest,
    UserSummary,
)
from .common import (
    ApiError,
    ErrorDetail,
)
from .readiness import (
    GapItem,
    ReadinessResponse,
    ReadinessSummary,
)
from .review import (
    ReviewNoteCreateRequest,
    ReviewNoteResponse,
    ReviewReadinessSummary,
    ReviewSnapshotResponse,
    ReviewStoryResponse,
    ReviewWorkspaceSnapshot,
)
from .story import (
    AcceptanceCriterionItem,
    StoryDraft,
    StorySaveResponse,
    StorySetUpdateRequest,
    ValidationSummary,
)
from .vision import VisionFields
from .workspace import (
    CompletenessInfo,
    ReviewSummary,
    StoryResponse,
    WorkspaceAggregate,
    WorkspaceAggregateResponse,
    WorkspaceSaveResponse,
    WorkspaceUpdateRequest,
)

__all__ = [
    "AcceptanceCriterionItem",
    "ApiError",
    "AuthResponse",
    "AuthTokenPayload",
    "CompletenessInfo",
    "ErrorDetail",
    "GapItem",
    "LoginRequest",
    "ReadinessResponse",
    "ReadinessSummary",
    "ReviewNoteCreateRequest",
    "ReviewNoteResponse",
    "ReviewReadinessSummary",
    "ReviewSnapshotResponse",
    "ReviewStoryResponse",
    "ReviewSummary",
    "ReviewWorkspaceSnapshot",
    "StoryDraft",
    "StoryResponse",
    "StorySaveResponse",
    "StorySetUpdateRequest",
    "UserSummary",
    "ValidationSummary",
    "VisionFields",
    "WorkspaceAggregate",
    "WorkspaceAggregateResponse",
    "WorkspaceSaveResponse",
    "WorkspaceUpdateRequest",
]

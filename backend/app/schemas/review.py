"""Review mode request and response schemas."""

from pydantic import BaseModel, Field, field_validator

from .vision import VisionFields


class ReviewNoteCreateRequest(BaseModel):
    """Request to create a review note.
    
    Used for POST /api/v1/review/{shareToken}/notes per LLD Section 4.11.
    Lightweight flat note model only.
    """
    reviewer_name: str = Field(
        ...,
        description="Reviewer name",
        min_length=2,
        max_length=80,
        alias="reviewerName"
    )
    note_text: str = Field(
        ...,
        description="Review note text",
        min_length=1,
        max_length=1000,
        alias="noteText"
    )

    @field_validator('reviewer_name')
    @classmethod
    def validate_reviewer_name_not_empty(cls, v: str) -> str:
        """Ensure reviewer name is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Reviewer name cannot be empty or whitespace only")
        return v

    @field_validator('note_text')
    @classmethod
    def validate_note_text_not_empty(cls, v: str) -> str:
        """Ensure note text is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Note text cannot be empty or whitespace only")
        return v

    class Config:
        populate_by_name = True


class ReviewNoteResponse(BaseModel):
    """Review note representation in responses.
    
    Per LLD Section 4.11, notes are flat with no threading.
    """
    id: int = Field(..., description="Note ID")
    reviewer_name: str = Field(..., description="Reviewer name", alias="reviewerName")
    note_text: str = Field(..., description="Note text", alias="noteText")
    created_at: str = Field(..., description="Note creation timestamp", alias="createdAt")

    class Config:
        populate_by_name = True
        from_attributes = True


class ReviewStoryResponse(BaseModel):
    """Story representation for review mode.
    
    Read-only projection with acceptance criteria.
    """
    title: str = Field(..., description="Story title")
    priority: str | None = Field(None, description="Story priority")
    acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="Acceptance criteria text list",
        alias="acceptanceCriteria"
    )

    class Config:
        populate_by_name = True


class ReviewReadinessSummary(BaseModel):
    """Readiness summary for review mode.
    
    Simplified version of ReadinessResponse for reviewer context.
    """
    status: str = Field(..., description="Readiness status")
    gaps: list[dict] = Field(default_factory=list, description="Gaps list")

    class Config:
        populate_by_name = True


class ReviewWorkspaceSnapshot(BaseModel):
    """Read-only workspace snapshot for review mode.
    
    Per LLD Section 4.10, review mode is read-focused and does not
    allow editing learner-owned core fields. Only review notes can be created.
    """
    product_name: str = Field(..., description="Product name", alias="productName")
    vision: VisionFields = Field(..., description="Vision and business context")
    stories: list[ReviewStoryResponse] = Field(default_factory=list, description="Stories")
    readiness: ReviewReadinessSummary = Field(..., description="Readiness status")
    review_notes: list[ReviewNoteResponse] = Field(
        default_factory=list,
        description="Review notes list",
        alias="reviewNotes"
    )

    class Config:
        populate_by_name = True


class ReviewSnapshotResponse(BaseModel):
    """Review mode snapshot response envelope.
    
    Response schema for GET /api/v1/review/{shareToken} per LLD Section 4.10.
    """
    workspace: ReviewWorkspaceSnapshot = Field(..., description="Workspace snapshot for review")

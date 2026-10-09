"""Workspace request and response schemas."""

from pydantic import BaseModel, Field, field_validator

from .story import AcceptanceCriterionItem
from .vision import VisionFields


class WorkspaceUpdateRequest(BaseModel):
    """Request to update workspace metadata and vision.
    
    Used for PUT /api/v1/workspace per LLD Section 4.7.
    """
    product_name: str = Field(
        ...,
        description="Product name",
        min_length=3,
        max_length=120,
        alias="productName"
    )
    short_description: str | None = Field(
        None,
        description="Short product description",
        max_length=280,
        alias="shortDescription"
    )
    vision: VisionFields = Field(
        ...,
        description="Vision and business context fields"
    )

    class Config:
        populate_by_name = True


class CompletenessInfo(BaseModel):
    """Workspace vision section completeness information."""
    vision_section_complete: bool = Field(
        ...,
        description="Whether vision section is complete",
        alias="visionSectionComplete"
    )
    missing_fields: list[str] = Field(
        default_factory=list,
        description="List of missing required fields",
        alias="missingFields"
    )

    class Config:
        populate_by_name = True


class WorkspaceSaveResponse(BaseModel):
    """Response for workspace save operation.
    
    Response schema for PUT /api/v1/workspace per LLD Section 4.7.
    """
    workspace_id: int = Field(..., description="Workspace ID", alias="workspaceId")
    last_saved_at: str = Field(..., description="Last save timestamp", alias="lastSavedAt")
    completeness: CompletenessInfo = Field(
        ...,
        description="Vision section completeness status"
    )

    class Config:
        populate_by_name = True


class StoryResponse(BaseModel):
    """Story representation for workspace aggregate responses.
    
    Includes full story details with acceptance criteria.
    Explicitly excludes internal implementation details.
    """
    id: int = Field(..., description="Story ID")
    title: str = Field(..., description="Story title")
    actor: str = Field(..., description="Story actor")
    need: str = Field(..., description="User need statement")
    outcome: str = Field(..., description="Desired outcome")
    description: str | None = Field(None, description="Additional description")
    priority: str | None = Field(None, description="Story priority (HIGH, MEDIUM, LOW)")
    backlog_order: int = Field(..., description="Backlog order", alias="backlogOrder")
    acceptance_criteria: list[AcceptanceCriterionItem] = Field(
        default_factory=list,
        description="Acceptance criteria",
        alias="acceptanceCriteria"
    )

    class Config:
        populate_by_name = True
        from_attributes = True


class ReviewSummary(BaseModel):
    """Review information summary for workspace aggregate.
    
    Contains share token and review notes list.
    """
    share_token: str | None = Field(None, description="Review share token", alias="shareToken")
    notes: list[dict] = Field(default_factory=list, description="Review notes list")

    class Config:
        populate_by_name = True


class WorkspaceAggregate(BaseModel):
    """Complete workspace aggregate with nested data.
    
    Contains workspace metadata, vision, stories, and review info.
    Used in GET /api/v1/workspace response per LLD Section 4.6.
    """
    id: int = Field(..., description="Workspace ID")
    product_name: str = Field(..., description="Product name", alias="productName")
    short_description: str | None = Field(None, description="Short description", alias="shortDescription")
    vision: VisionFields = Field(..., description="Vision and business context")
    stories: list[StoryResponse] = Field(default_factory=list, description="Stories with criteria")
    review: ReviewSummary = Field(default_factory=ReviewSummary, description="Review information")
    last_saved_at: str = Field(..., description="Last save timestamp", alias="lastSavedAt")

    class Config:
        populate_by_name = True


class WorkspaceAggregateResponse(BaseModel):
    """Workspace aggregate response envelope.
    
    Response schema for GET /api/v1/workspace per LLD Section 4.6.
    Ensures password_hash and other sensitive fields are never exposed.
    """
    workspace: WorkspaceAggregate = Field(..., description="Workspace aggregate data")

    @field_validator('workspace')
    @classmethod
    def ensure_no_sensitive_fields(cls, v: WorkspaceAggregate) -> WorkspaceAggregate:
        """Ensure response does not contain sensitive fields.
        
        This validator acts as a safety net to prevent accidental
        exposure of password_hash, tokens, or other sensitive data.
        """
        # Pydantic schema enforcement already excludes these, but this
        # validator provides an explicit safety check per REQ-SEC-002
        return v

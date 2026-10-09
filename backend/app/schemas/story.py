"""Story and acceptance criteria schemas."""
from pydantic import BaseModel, Field, field_validator


class AcceptanceCriterionItem(BaseModel):
    """Acceptance criterion for a story.
    
    May include id for existing criteria or omit for new criteria.
    Per LLD Section 4.8 and 9.3.
    """
    id: int | None = Field(None, description="Criterion ID (null for new criteria)")
    text: str = Field(
        ...,
        description="Acceptance criterion text",
        min_length=1,
        max_length=500
    )

    class Config:
        from_attributes = True


class StoryDraft(BaseModel):
    """Story draft for create/update operations.
    
    Used in PUT /api/v1/workspace/stories request per LLD Section 4.8.
    Preserves recognizable story format using actor, need, outcome fields.
    """
    id: int | None = Field(None, description="Story ID (null for new stories)")
    title: str = Field(
        ...,
        description="Story title",
        min_length=1,
        max_length=200
    )
    actor: str = Field(
        ...,
        description="Story actor (user role)",
        min_length=1
    )
    need: str = Field(
        ...,
        description="User need statement",
        min_length=1,
        alias="need"
    )
    outcome: str = Field(
        ...,
        description="Desired outcome statement",
        min_length=1,
        alias="outcome"
    )
    description: str | None = Field(
        None,
        description="Additional story description"
    )
    priority: str | None = Field(
        None,
        description="Story priority (HIGH, MEDIUM, LOW, or null during drafting)"
    )
    backlog_order: int = Field(
        ...,
        description="Backlog order (positive integer, unique within workspace)",
        gt=0,
        alias="backlogOrder"
    )
    acceptance_criteria: list[AcceptanceCriterionItem] = Field(
        default_factory=list,
        description="Acceptance criteria list",
        alias="acceptanceCriteria"
    )

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: str | None) -> str | None:
        """Validate priority enum if provided."""
        if v is not None and v not in ("HIGH", "MEDIUM", "LOW"):
            raise ValueError("Priority must be HIGH, MEDIUM, or LOW")
        return v

    class Config:
        populate_by_name = True
        from_attributes = True


class StorySetUpdateRequest(BaseModel):
    """Request to upsert the full editable story set.
    
    Used for PUT /api/v1/workspace/stories per LLD Section 4.8.
    Story omissions represent deletes after client confirmation.
    """
    stories: list[StoryDraft] = Field(
        ...,
        description="Full story set with ordering and criteria"
    )

    @field_validator('stories')
    @classmethod
    def validate_story_count(cls, v: list[StoryDraft]) -> list[StoryDraft]:
        """Validate story list bounds per LLD Section 4.8."""
        if len(v) > 20:
            raise ValueError("Maximum 20 stories allowed for MVP manageability")
        return v


class ValidationSummary(BaseModel):
    """Summary of validation issues in story set."""
    stories_missing_priority: int = Field(
        ...,
        description="Count of stories without priority",
        alias="storiesMissingPriority"
    )
    stories_missing_acceptance_criteria: int = Field(
        ...,
        description="Count of stories without acceptance criteria",
        alias="storiesMissingAcceptanceCriteria"
    )

    class Config:
        populate_by_name = True


class StorySaveResponse(BaseModel):
    """Response for story set save operation.
    
    Response schema for PUT /api/v1/workspace/stories per LLD Section 4.8.
    """
    workspace_id: int = Field(..., description="Workspace ID", alias="workspaceId")
    stories_saved: int = Field(..., description="Number of stories saved", alias="storiesSaved")
    last_saved_at: str = Field(..., description="Last save timestamp", alias="lastSavedAt")
    validation_summary: ValidationSummary = Field(
        ...,
        description="Validation summary for readiness",
        alias="validationSummary"
    )

    class Config:
        populate_by_name = True

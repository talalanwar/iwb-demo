"""Readiness evaluation response schemas."""
from pydantic import BaseModel, Field


class GapItem(BaseModel):
    """Individual readiness gap with navigation target.
    
    Per LLD Section 4.9 and 6.3, each gap includes deterministic
    navigation target for the React router.
    """
    code: str = Field(..., description="Gap code (e.g. MISSING_PRIORITY)")
    message: str = Field(..., description="Human-readable gap description")
    navigate_to: str = Field(
        ...,
        description="Navigation target for fixing the gap",
        alias="navigateTo"
    )

    class Config:
        populate_by_name = True


class ReadinessSummary(BaseModel):
    """Summary of workspace completeness metrics.
    
    Per LLD Section 4.9, provides counts and flags for readiness evaluation.
    """
    vision_complete: bool = Field(
        ...,
        description="All required vision fields populated",
        alias="visionComplete"
    )
    business_goals_count: int = Field(
        ...,
        description="Number of business goals defined",
        alias="businessGoalsCount"
    )
    story_count: int = Field(
        ...,
        description="Total number of stories",
        alias="storyCount"
    )
    stories_with_acceptance_criteria: int = Field(
        ...,
        description="Number of stories with at least one acceptance criterion",
        alias="storiesWithAcceptanceCriteria"
    )
    stories_with_priority: int = Field(
        ...,
        description="Number of stories with assigned priority",
        alias="storiesWithPriority"
    )
    review_notes_count: int = Field(
        ...,
        description="Number of review notes",
        alias="reviewNotesCount"
    )

    class Config:
        populate_by_name = True


class ReadinessResponse(BaseModel):
    """Readiness evaluation response.
    
    Response schema for GET /api/v1/workspace/readiness per LLD Section 4.9.
    Status derived from readiness algorithm in LLD Section 6.2.
    """
    workspace_id: int = Field(..., description="Workspace ID", alias="workspaceId")
    status: str = Field(
        ...,
        description=(
            "Readiness status: NOT_STARTED, IN_PROGRESS, "
            "NEEDS_ATTENTION, or READY_FOR_REVIEW"
        )
    )
    summary: ReadinessSummary = Field(..., description="Completeness summary metrics")
    gaps: list[GapItem] = Field(default_factory=list, description="List of detected gaps")
    release_readiness_interpretation: str = Field(
        ...,
        description=(
            "Interpretation of release readiness per Product Spec binding rules. "
            "All included stories must have acceptance criteria and assigned "
            "priorities before review-ready interpretation is met."
        ),
        alias="releaseReadinessInterpretation"
    )

    class Config:
        populate_by_name = True

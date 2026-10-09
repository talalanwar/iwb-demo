"""Vision and business context schemas."""
from pydantic import BaseModel, Field, field_validator


class VisionFields(BaseModel):
    """Vision section fields for product definition.
    
    Contains vision statement, target problem, business goals, and success measures.
    Used within workspace payloads per LLD Section 4.6 and 4.7.
    """
    vision_statement: str | None = Field(
        None,
        description="Product vision statement",
        max_length=1000,
        alias="visionStatement"
    )
    target_problem: str | None = Field(
        None,
        description="Target problem the product solves",
        max_length=1000,
        alias="targetProblem"
    )
    business_goals: list[str] = Field(
        default_factory=list,
        description="Business goals (min 1 for completeness, max 5)",
        alias="businessGoals"
    )
    success_measures: list[str] = Field(
        default_factory=list,
        description="Success measures (min 1 for completeness, max 5)",
        alias="successMeasures"
    )

    @field_validator('business_goals')
    @classmethod
    def validate_business_goals_length(cls, v: list[str]) -> list[str]:
        """Validate business goals array bounds per LLD Section 6.1."""
        if len(v) > 5:
            raise ValueError("Maximum 5 business goals allowed")
        return v

    @field_validator('success_measures')
    @classmethod
    def validate_success_measures_length(cls, v: list[str]) -> list[str]:
        """Validate success measures array bounds per LLD Section 6.1."""
        if len(v) > 5:
            raise ValueError("Maximum 5 success measures allowed")
        return v

    class Config:
        populate_by_name = True


class CompletenessInfo(BaseModel):
    """Vision section completeness information."""
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


class VisionSaveResponse(BaseModel):
    """Response for workspace metadata and vision save operation.
    
    Response schema for PUT /api/v1/workspace per LLD Section 4.7.
    """
    workspace_id: int = Field(..., description="Workspace ID", alias="workspaceId")
    last_saved_at: str = Field(..., description="Last save timestamp", alias="lastSavedAt")
    completeness: CompletenessInfo = Field(
        ...,
        description="Vision completeness info for readiness tracking"
    )

    class Config:
        populate_by_name = True

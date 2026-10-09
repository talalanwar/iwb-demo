"""Workspace routes for workspace lifecycle, vision, stories, and readiness."""
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_auth
from app.core.database import get_db
from app.models.user import User
from app.schemas.readiness import ReadinessResponse
from app.schemas.story import StorySaveResponse, StorySetUpdateRequest
from app.schemas.vision import VisionSaveResponse
from app.schemas.workspace import WorkspaceAggregateResponse, WorkspaceUpdateRequest
from app.services.readiness_service import ReadinessService
from app.services.story_service import StoryService
from app.services.vision_service import VisionService
from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("", response_model=WorkspaceAggregateResponse, status_code=status.HTTP_200_OK)
def get_workspace(
    current_user: Annotated[User, Depends(require_auth)],
    db: Annotated[Session, Depends(get_db)]
) -> WorkspaceAggregateResponse:
    """Create or open the authenticated learner's single workspace aggregate.
    
    Args:
        current_user: Authenticated user from token
        db: Database session
        
    Returns:
        WorkspaceAggregateResponse with complete workspace data
    """
    workspace_service = WorkspaceService(db)
    
    # Create or open workspace
    workspace = workspace_service.create_or_open_workspace(current_user.id)
    
    # Assemble aggregate payload
    aggregate = workspace_service.assemble_workspace_aggregate(workspace)
    
    return WorkspaceAggregateResponse(workspace=aggregate)


@router.put("", response_model=VisionSaveResponse, status_code=status.HTTP_200_OK)
def update_workspace(
    request: WorkspaceUpdateRequest,
    current_user: Annotated[User, Depends(require_auth)],
    db: Annotated[Session, Depends(get_db)]
) -> VisionSaveResponse:
    """Save workspace metadata and vision/business context.
    
    Args:
        request: Workspace update payload with metadata and vision
        current_user: Authenticated user from token
        db: Database session
        
    Returns:
        VisionSaveResponse with save confirmation and completeness info
    """
    workspace_service = WorkspaceService(db)
    vision_service = VisionService(db)
    
    # Get workspace
    workspace = workspace_service.create_or_open_workspace(current_user.id)
    
    # Update metadata and vision
    updated_workspace = vision_service.save_workspace_metadata_and_vision(
        workspace=workspace,
        product_name=request.productName,
        short_description=request.shortDescription,
        vision_statement=request.vision.visionStatement,
        target_problem=request.vision.targetProblem,
        business_goals=request.vision.businessGoals,
        success_measures=request.vision.successMeasures
    )
    
    db.commit()
    
    # Evaluate completeness
    completeness_info = vision_service.evaluate_vision_completeness(updated_workspace)
    
    return VisionSaveResponse(
        workspaceId=updated_workspace.id,
        lastSavedAt=updated_workspace.updated_at,
        completeness=completeness_info
    )


@router.put("/stories", response_model=StorySaveResponse, status_code=status.HTTP_200_OK)
def update_stories(
    request: StorySetUpdateRequest,
    current_user: Annotated[User, Depends(require_auth)],
    db: Annotated[Session, Depends(get_db)]
) -> StorySaveResponse:
    """Upsert the full editable story set and backlog ordering.
    
    Args:
        request: Story set update payload with full story list
        current_user: Authenticated user from token
        db: Database session
        
    Returns:
        StorySaveResponse with save confirmation and validation summary
    """
    workspace_service = WorkspaceService(db)
    story_service = StoryService(db)
    
    # Get workspace
    workspace = workspace_service.create_or_open_workspace(current_user.id)
    
    # Upsert stories
    stories_saved, validation_summary = story_service.upsert_story_set(
        workspace=workspace,
        stories_data=request.stories
    )
    
    db.commit()
    
    return StorySaveResponse(
        workspaceId=workspace.id,
        storiesSaved=stories_saved,
        lastSavedAt=workspace.updated_at,
        validationSummary=validation_summary
    )


@router.get("/readiness", response_model=ReadinessResponse, status_code=status.HTTP_200_OK)
def get_readiness(
    current_user: Annotated[User, Depends(require_auth)],
    db: Annotated[Session, Depends(get_db)]
) -> ReadinessResponse:
    """Compute summary of coherence and missing essentials before review handoff.
    
    Args:
        current_user: Authenticated user from token
        db: Database session
        
    Returns:
        ReadinessResponse with status, summary, and navigable gaps
    """
    workspace_service = WorkspaceService(db)
    readiness_service = ReadinessService(db)
    
    # Get workspace with relationships
    workspace = workspace_service.create_or_open_workspace(current_user.id)
    
    # Evaluate readiness
    readiness_response = readiness_service.evaluate_readiness(workspace)
    
    return readiness_response

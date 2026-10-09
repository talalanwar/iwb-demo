"""Review routes for protected review mode and review notes."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.review import (
    ReviewNoteCreateRequest,
    ReviewNoteResponse,
    ReviewSnapshotResponse,
)
from app.services.review_service import ReviewService

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/{shareToken}", response_model=ReviewSnapshotResponse, status_code=status.HTTP_200_OK)
def get_review_snapshot(
    shareToken: str,
    db: Annotated[Session, Depends(get_db)]
) -> ReviewSnapshotResponse:
    """Return protected review-mode snapshot.
    
    Args:
        shareToken: Protected share token for review access
        db: Database session
        
    Returns:
        ReviewSnapshotResponse with read-focused workspace snapshot
        
    Raises:
        HTTPException: 404 if token is invalid or workspace not found
        HTTPException: 403 if token is expired or access is denied
    """
    review_service = ReviewService(db)
    
    # Validate token and get workspace
    workspace = review_service.validate_and_get_workspace(shareToken)
    
    # Assemble review snapshot
    snapshot = review_service.create_review_snapshot(workspace)
    
    return ReviewSnapshotResponse(workspace=snapshot)


@router.post("/{shareToken}/notes", response_model=ReviewNoteResponse, status_code=status.HTTP_201_CREATED)
def create_review_note(
    shareToken: str,
    request: ReviewNoteCreateRequest,
    db: Annotated[Session, Depends(get_db)]
) -> ReviewNoteResponse:
    """Save concise reviewer feedback.
    
    Args:
        shareToken: Protected share token for review access
        request: Review note payload with reviewer name and note text
        db: Database session
        
    Returns:
        ReviewNoteResponse with saved note details
        
    Raises:
        HTTPException: 404 if token is invalid or workspace not found
        HTTPException: 403 if token is expired or access is denied
    """
    review_service = ReviewService(db)
    
    # Validate token and get workspace
    workspace = review_service.validate_and_get_workspace(shareToken)
    
    # Save review note
    note = review_service.create_review_note(
        workspace=workspace,
        reviewer_name=request.reviewerName,
        note_text=request.noteText
    )
    
    db.commit()
    
    return ReviewNoteResponse(
        note={
            "id": note["id"],
            "reviewerName": note["reviewerName"],
            "noteText": note["noteText"],
            "createdAt": note["createdAt"]
        }
    )

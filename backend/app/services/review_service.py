"""Review service for share token validation and review note persistence."""
import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.logging import get_logger, log_review_action
from app.domain.share_access import generate_share_token, validate_share_token
from app.models.workspace import Workspace
from app.repositories.review_repository import ReviewRepository
from app.repositories.workspace_repository import WorkspaceRepository

logger = get_logger(__name__)


class ReviewService:
    """Service for review operations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
        self.review_repo = ReviewRepository(db)
        self.workspace_repo = WorkspaceRepository(db)
    
    def validate_and_get_workspace(self, share_token: str) -> Workspace:
        """Validate share token and return workspace.
        
        Args:
            share_token: Share token string
            
        Returns:
            Workspace instance if token is valid
            
        Raises:
            HTTPException: 403/404 if token is invalid or unauthorized
        """
        # Validate token format
        if not validate_share_token(share_token):
            log_review_action(
                logger=logger,
                action_type="access_denied",
                workspace_id="unknown"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review access invalid."
            )
        
        # Fetch review share
        review_share = self.review_repo.get_share_by_token(share_token)
        
        if not review_share:
            log_review_action(
                logger=logger,
                action_type="access_denied",
                workspace_id="unknown"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review access invalid."
            )
        
        # Fetch workspace
        workspace = self.workspace_repo.get_by_owner(review_share.workspace.owner_user_id)
        
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found."
            )
        
        log_review_action(
            logger=logger,
            action_type="access_granted",
            workspace_id=str(workspace.id)
        )
        
        return workspace
    
    def create_review_snapshot(self, workspace: Workspace) -> dict:
        """Create review-mode snapshot payload.
        
        Args:
            workspace: Workspace instance with eager-loaded relationships
            
        Returns:
            Dictionary with review-focused workspace data
        """
        # Parse JSON fields
        business_goals = json.loads(workspace.business_goals_json)
        success_measures = json.loads(workspace.success_measures_json)
        
        # Build vision section
        vision = {
            "visionStatement": workspace.vision_statement,
            "targetProblem": workspace.target_problem,
            "businessGoals": business_goals,
            "successMeasures": success_measures
        }
        
        # Build stories
        stories = []
        for story in workspace.stories:
            criteria = [c.criterion_text for c in story.criteria]
            stories.append({
                "title": story.title,
                "actor": story.actor,
                "need": story.need_text,
                "outcome": story.outcome_text,
                "priority": story.priority,
                "acceptanceCriteria": criteria
            })
        
        # Build readiness summary (simplified for review mode)
        stories_with_criteria = sum(1 for s in workspace.stories if s.criteria and len(s.criteria) > 0)
        stories_with_priority = sum(1 for s in workspace.stories if s.priority)
        all_complete = (
            stories_with_criteria == len(workspace.stories) and
            stories_with_priority == len(workspace.stories)
        )
        
        readiness = {
            "status": "READY_FOR_REVIEW" if all_complete else "NEEDS_ATTENTION",
            "gaps": []
        }
        
        # Build review notes
        review_notes = []
        for note in workspace.review_notes:
            review_notes.append({
                "id": note.id,
                "reviewerName": note.reviewer_name,
                "noteText": note.note_text,
                "createdAt": note.created_at.isoformat() if note.created_at else None
            })
        
        return {
            "productName": workspace.product_name,
            "vision": vision,
            "stories": stories,
            "readiness": readiness,
            "reviewNotes": review_notes
        }
    
    def create_review_note(
        self,
        workspace: Workspace,
        reviewer_name: str,
        note_text: str
    ) -> dict:
        """Save review note.
        
        Args:
            workspace: Workspace instance
            reviewer_name: Reviewer name
            note_text: Note text content
            
        Returns:
            Dictionary with created note data
        """
        note = self.review_repo.create_note(
            workspace_id=workspace.id,
            reviewer_name=reviewer_name,
            note_text=note_text
        )
        
        self.db.commit()
        
        log_review_action(
            logger=logger,
            action_type="note_created",
            workspace_id=str(workspace.id),
            reviewer_name=reviewer_name
        )
        
        return {
            "id": note.id,
            "reviewerName": note.reviewer_name,
            "noteText": note.note_text,
            "createdAt": note.created_at.isoformat() if note.created_at else None
        }
    
    def ensure_share_token(self, workspace: Workspace, created_by_user_id: int) -> str:
        """Ensure workspace has a review share token.
        
        Args:
            workspace: Workspace instance
            created_by_user_id: User ID creating the share
            
        Returns:
            Share token string
        """
        # Check if share already exists
        existing_share = self.review_repo.get_share_by_workspace(workspace.id)
        
        if existing_share:
            return existing_share.share_token
        
        # Generate new share token
        share_token = generate_share_token()
        
        self.review_repo.create_share(
            workspace_id=workspace.id,
            share_token=share_token,
            created_by_user_id=created_by_user_id,
            requires_auth=True
        )
        
        self.db.commit()
        
        return share_token

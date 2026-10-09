"""Workspace service for workspace lifecycle and aggregate assembly."""
import json

from sqlalchemy.orm import Session

from app.core.logging import get_logger, log_save_event
from app.models.workspace import Workspace
from app.repositories.workspace_repository import WorkspaceRepository

logger = get_logger(__name__)


class WorkspaceService:
    """Service for workspace operations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
        self.workspace_repo = WorkspaceRepository(db)
    
    def create_or_open_workspace(self, owner_user_id: int) -> Workspace:
        """Create or open the single workspace for a user.
        
        Enforces one workspace per user per MVP scope.
        
        Args:
            owner_user_id: Owner user ID
            
        Returns:
            Workspace instance (existing or newly created)
        """
        # Check if workspace already exists
        workspace = self.workspace_repo.get_by_owner(owner_user_id)
        
        if workspace:
            return workspace
        
        # Create new workspace with defaults
        workspace = self.workspace_repo.create(
            owner_user_id=owner_user_id,
            product_name="Untitled Product",
            short_description=None
        )
        
        self.db.commit()
        
        log_save_event(
            logger=logger,
            resource_type="workspace",
            resource_id=str(workspace.id),
            user_id=owner_user_id,
            operation="create"
        )
        
        return workspace
    
    def assemble_workspace_aggregate(self, workspace: Workspace) -> dict:
        """Assemble complete workspace aggregate payload.
        
        Args:
            workspace: Workspace instance with eager-loaded relationships
            
        Returns:
            Dictionary with complete workspace aggregate data
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
        
        # Build stories with acceptance_criteria
        stories = []
        for story in workspace.stories:
            criteria = []
            for criterion in story.acceptance_criteria:
                criteria.append({
                    "id": criterion.id,
                    "text": criterion.criterion_text
                })
            
            stories.append({
                "id": story.id,
                "title": story.title,
                "actor": story.actor,
                "need": story.need_text,
                "outcome": story.outcome_text,
                "description": story.description,
                "priority": story.priority,
                "backlogOrder": story.backlog_order,
                "acceptanceCriteria": criteria
            })
        
        # Build review summary
        review = {
            "shareToken": workspace.review_share.share_token if workspace.review_share else None,
            "notes": []
        }
        
        for note in workspace.review_notes:
            review["notes"].append({
                "id": note.id,
                "reviewerName": note.reviewer_name,
                "noteText": note.note_text,
                "createdAt": note.created_at.isoformat() if note.created_at else None
            })
        
        # Assemble complete aggregate
        aggregate = {
            "id": workspace.id,
            "productName": workspace.product_name,
            "shortDescription": workspace.short_description,
            "vision": vision,
            "stories": stories,
            "review": review,
            "lastSavedAt": workspace.updated_at.isoformat() if workspace.updated_at else None
        }
        
        return aggregate
    
    def update_workspace_metadata_and_vision(
        self,
        workspace: Workspace,
        product_name: str | None = None,
        short_description: str | None = None,
        vision_statement: str | None = None,
        target_problem: str | None = None,
        business_goals: list[str] | None = None,
        success_measures: list[str] | None = None
    ) -> Workspace:
        """Update workspace metadata and vision fields.
        
        Args:
            workspace: Workspace instance to update
            product_name: Optional product name
            short_description: Optional short description
            vision_statement: Optional vision statement
            target_problem: Optional target problem
            business_goals: Optional business goals array
            success_measures: Optional success measures array
            
        Returns:
            Updated Workspace instance
        """
        workspace = self.workspace_repo.update_metadata_and_vision(
            workspace=workspace,
            product_name=product_name,
            short_description=short_description,
            vision_statement=vision_statement,
            target_problem=target_problem,
            business_goals=business_goals,
            success_measures=success_measures
        )
        
        self.db.commit()
        
        log_save_event(
            logger=logger,
            resource_type="workspace",
            resource_id=str(workspace.id),
            user_id=workspace.owner_user_id,
            operation="update"
        )
        
        return workspace

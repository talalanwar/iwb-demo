"""Vision service for vision persistence and completeness tracking."""
import json

from sqlalchemy.orm import Session

from app.core.logging import get_logger, log_save_event
from app.models.workspace import Workspace
from app.repositories.workspace_repository import WorkspaceRepository

logger = get_logger(__name__)


class VisionService:
    """Service for vision operations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
        self.workspace_repo = WorkspaceRepository(db)
    
    def save_vision(
        self,
        workspace: Workspace,
        vision_statement: str | None = None,
        target_problem: str | None = None,
        business_goals: list[str] | None = None,
        success_measures: list[str] | None = None
    ) -> Workspace:
        """Save vision and business context fields.
        
        Args:
            workspace: Workspace instance to update
            vision_statement: Optional vision statement
            target_problem: Optional target problem
            business_goals: Optional business goals array
            success_measures: Optional success measures array
            
        Returns:
            Updated Workspace instance
        """
        workspace = self.workspace_repo.update_metadata_and_vision(
            workspace=workspace,
            vision_statement=vision_statement,
            target_problem=target_problem,
            business_goals=business_goals,
            success_measures=success_measures
        )
        
        # Update status if transitioning from EMPTY
        if workspace.status == "EMPTY" and (vision_statement or target_problem):
            workspace = self.workspace_repo.update_status(workspace, "DRAFTING_VISION")
        
        self.db.commit()
        
        log_save_event(
            logger=logger,
            resource_type="vision",
            resource_id=str(workspace.id),
            user_id=workspace.owner_user_id,
            operation="update"
        )
        
        return workspace
    
    def check_vision_completeness(self, workspace: Workspace) -> dict:
        """Check vision section completeness and identify missing fields.
        
        Args:
            workspace: Workspace instance
            
        Returns:
            Dictionary with completeness status and missing fields
        """
        missing_fields = []
        
        if not workspace.vision_statement:
            missing_fields.append("visionStatement")
        
        if not workspace.target_problem:
            missing_fields.append("targetProblem")
        
        business_goals = json.loads(workspace.business_goals_json)
        if len(business_goals) < 1:
            missing_fields.append("businessGoals")
        
        success_measures = json.loads(workspace.success_measures_json)
        if len(success_measures) < 1:
            missing_fields.append("successMeasures")
        
        vision_complete = len(missing_fields) == 0
        
        return {
            "visionSectionComplete": vision_complete,
            "missingFields": missing_fields
        }
    
    def save_workspace_metadata_and_vision(
        self,
        workspace: Workspace,
        product_name: str | None = None,
        short_description: str | None = None,
        vision_statement: str | None = None,
        target_problem: str | None = None,
        business_goals: list[str] | None = None,
        success_measures: list[str] | None = None
    ) -> Workspace:
        """Save workspace metadata and vision fields together.
        
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
        
        # Update status if transitioning from EMPTY
        if workspace.status == "EMPTY" and (vision_statement or target_problem or product_name):
            workspace = self.workspace_repo.update_status(workspace, "DRAFTING_VISION")
        
        log_save_event(
            logger=logger,
            resource_type="workspace",
            resource_id=str(workspace.id),
            user_id=workspace.owner_user_id,
            operation="update"
        )
        
        return workspace
    
    def evaluate_vision_completeness(self, workspace: Workspace) -> dict:
        """Evaluate vision section completeness.
        
        Alias for check_vision_completeness for consistency with route naming.
        
        Args:
            workspace: Workspace instance
            
        Returns:
            Dictionary with completeness status and missing fields
        """
        return self.check_vision_completeness(workspace)

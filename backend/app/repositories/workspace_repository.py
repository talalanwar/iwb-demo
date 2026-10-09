"""Repository for Workspace model persistence operations."""
import json

from sqlalchemy.orm import Session, joinedload

from app.models.story import Story
from app.models.workspace import Workspace


class WorkspaceRepository:
    """Repository for Workspace model data access."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
    
    def get_by_owner(self, owner_user_id: int) -> Workspace | None:
        """Fetch workspace by owner user ID with eager-loaded relationships.
        
        Args:
            owner_user_id: Owner user ID
            
        Returns:
            Workspace instance if found, None otherwise
        """
        return self.db.query(Workspace).filter(
            Workspace.owner_user_id == owner_user_id
        ).options(
            joinedload(Workspace.stories).joinedload(Story.acceptance_criteria),
            joinedload(Workspace.review_share),
            joinedload(Workspace.review_notes)
        ).first()
    
    def create(
        self, 
        owner_user_id: int, 
        product_name: str = "Untitled Product",
        short_description: str | None = None
    ) -> Workspace:
        """Create a new workspace.
        
        Args:
            owner_user_id: Owner user ID
            product_name: Product name (defaults to "Untitled Product")
            short_description: Optional short description
            
        Returns:
            Created Workspace instance
        """
        workspace = Workspace(
            owner_user_id=owner_user_id,
            product_name=product_name,
            short_description=short_description,
            business_goals_json="[]",
            success_measures_json="[]",
            status="EMPTY"
        )
        self.db.add(workspace)
        self.db.flush()
        return workspace
    
    def update_metadata_and_vision(
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
        if product_name is not None:
            workspace.product_name = product_name
        if short_description is not None:
            workspace.short_description = short_description
        if vision_statement is not None:
            workspace.vision_statement = vision_statement
        if target_problem is not None:
            workspace.target_problem = target_problem
        if business_goals is not None:
            workspace.business_goals_json = json.dumps(business_goals)
        if success_measures is not None:
            workspace.success_measures_json = json.dumps(success_measures)
        
        self.db.flush()
        return workspace
    
    def update_status(self, workspace: Workspace, status: str) -> Workspace:
        """Update workspace status.
        
        Args:
            workspace: Workspace instance to update
            status: New status
            
        Returns:
            Updated Workspace instance
        """
        workspace.status = status
        self.db.flush()
        return workspace

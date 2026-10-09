"""Story service for story CRUD, criteria management, and priority assignment."""
from sqlalchemy.orm import Session

from app.core.logging import get_logger, log_save_event
from app.models.workspace import Workspace
from app.repositories.story_repository import StoryRepository
from app.repositories.workspace_repository import WorkspaceRepository

logger = get_logger(__name__)


class StoryService:
    """Service for story operations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
        self.story_repo = StoryRepository(db)
        self.workspace_repo = WorkspaceRepository(db)
    
    def upsert_story_set(
        self,
        workspace: Workspace,
        stories_data: list[dict]
    ) -> tuple[int, dict]:
        """Upsert full editable story set.
        
        Implements bulk story update per LLD Section 4.8.
        Stories omitted from the submitted set are deleted.
        
        Args:
            workspace: Workspace instance
            stories_data: List of story dictionaries with fields:
                - id (optional): Story ID for update
                - title: Story title
                - actor: Story actor
                - need: Story need text
                - outcome: Story outcome text
                - description (optional): Story description
                - priority (optional): Story priority
                - backlogOrder: Backlog order position
                - acceptanceCriteria: List of criterion dictionaries
                
        Returns:
            Tuple of (stories_saved_count, validation_summary)
        """
        # Track submitted story IDs
        submitted_ids = set()
        stories_missing_priority = 0
        stories_missing_criteria = 0
        
        # Process each story in the submitted set
        for story_data in stories_data:
            story_id = story_data.get("id")
            
            if story_id:
                submitted_ids.add(story_id)
                # Update existing story
                story = self.story_repo.get_by_id(story_id)
                if story and story.workspace_id == workspace.id:
                    story = self.story_repo.update_story(
                        story=story,
                        title=story_data.get("title"),
                        actor=story_data.get("actor"),
                        need_text=story_data.get("need"),
                        outcome_text=story_data.get("outcome"),
                        description=story_data.get("description"),
                        priority=story_data.get("priority"),
                        backlog_order=story_data.get("backlogOrder")
                    )
            else:
                # Create new story
                story = self.story_repo.create_story(
                    workspace_id=workspace.id,
                    title=story_data["title"],
                    actor=story_data["actor"],
                    need_text=story_data["need"],
                    outcome_text=story_data["outcome"],
                    description=story_data.get("description"),
                    priority=story_data.get("priority"),
                    backlog_order=story_data["backlogOrder"]
                )
                submitted_ids.add(story.id)
            
            # Update acceptance criteria
            self.story_repo.delete_criteria_for_story(story.id)
            criteria_list = story_data.get("acceptanceCriteria", [])
            
            for idx, criterion_data in enumerate(criteria_list):
                self.story_repo.create_criterion(
                    story_id=story.id,
                    criterion_text=criterion_data["text"],
                    display_order=idx + 1
                )
            
            # Track validation summary
            if not story.priority:
                stories_missing_priority += 1
            if len(criteria_list) == 0:
                stories_missing_criteria += 1
        
        # Delete stories not in submitted set
        existing_stories = self.story_repo.get_by_workspace(workspace.id)
        for existing_story in existing_stories:
            if existing_story.id not in submitted_ids:
                self.story_repo.delete_story(existing_story)
        
        # Update workspace status if transitioning
        if workspace.status == "EMPTY" or workspace.status == "DRAFTING_VISION":
            workspace = self.workspace_repo.update_status(workspace, "DRAFTING_BACKLOG")
        
        self.db.commit()
        
        log_save_event(
            logger=logger,
            resource_type="stories",
            resource_id=str(workspace.id),
            user_id=workspace.owner_user_id,
            operation="update"
        )
        
        validation_summary = {
            "storiesMissingPriority": stories_missing_priority,
            "storiesMissingAcceptanceCriteria": stories_missing_criteria
        }
        
        return len(stories_data), validation_summary
    
    def get_ordered_backlog(self, workspace_id: int) -> list:
        """Get stories ordered by backlog_order.
        
        Args:
            workspace_id: Workspace ID
            
        Returns:
            List of Story instances ordered by backlog_order
        """
        return self.story_repo.get_by_workspace(workspace_id)

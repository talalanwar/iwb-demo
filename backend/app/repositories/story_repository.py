"""Repository for Story and AcceptanceCriterion model persistence operations."""
from sqlalchemy.orm import Session

from app.models.acceptance_criterion import AcceptanceCriterion
from app.models.story import Story


class StoryRepository:
    """Repository for Story and AcceptanceCriterion model data access."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
    
    def get_by_id(self, story_id: int) -> Story | None:
        """Fetch story by ID.
        
        Args:
            story_id: Story ID
            
        Returns:
            Story instance if found, None otherwise
        """
        return self.db.query(Story).filter(Story.id == story_id).first()
    
    def get_by_workspace(self, workspace_id: int) -> list[Story]:
        """Fetch all stories for a workspace ordered by backlog_order.
        
        Args:
            workspace_id: Workspace ID
            
        Returns:
            List of Story instances
        """
        return self.db.query(Story).filter(
            Story.workspace_id == workspace_id
        ).order_by(Story.backlog_order).all()
    
    def create_story(
        self,
        workspace_id: int,
        title: str,
        actor: str,
        need_text: str,
        outcome_text: str,
        description: str | None = None,
        priority: str | None = None,
        backlog_order: int = 1
    ) -> Story:
        """Create a new story.
        
        Args:
            workspace_id: Workspace ID
            title: Story title
            actor: Story actor
            need_text: Story need
            outcome_text: Story outcome
            description: Optional story description
            priority: Optional priority (HIGH, MEDIUM, LOW)
            backlog_order: Backlog order position
            
        Returns:
            Created Story instance
        """
        story = Story(
            workspace_id=workspace_id,
            title=title,
            actor=actor,
            need_text=need_text,
            outcome_text=outcome_text,
            description=description,
            priority=priority,
            backlog_order=backlog_order
        )
        self.db.add(story)
        self.db.flush()
        return story
    
    def update_story(
        self,
        story: Story,
        title: str | None = None,
        actor: str | None = None,
        need_text: str | None = None,
        outcome_text: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        backlog_order: int | None = None
    ) -> Story:
        """Update an existing story.
        
        Args:
            story: Story instance to update
            title: Optional new title
            actor: Optional new actor
            need_text: Optional new need text
            outcome_text: Optional new outcome text
            description: Optional new description
            priority: Optional new priority
            backlog_order: Optional new backlog order
            
        Returns:
            Updated Story instance
        """
        if title is not None:
            story.title = title
        if actor is not None:
            story.actor = actor
        if need_text is not None:
            story.need_text = need_text
        if outcome_text is not None:
            story.outcome_text = outcome_text
        if description is not None:
            story.description = description
        if priority is not None:
            story.priority = priority
        if backlog_order is not None:
            story.backlog_order = backlog_order
        
        self.db.flush()
        return story
    
    def delete_story(self, story: Story) -> None:
        """Delete a story (cascade deletes criteria).
        
        Args:
            story: Story instance to delete
        """
        self.db.delete(story)
        self.db.flush()
    
    def delete_criteria_for_story(self, story_id: int) -> None:
        """Delete all acceptance criteria for a story.
        
        Args:
            story_id: Story ID
        """
        self.db.query(AcceptanceCriterion).filter(
            AcceptanceCriterion.story_id == story_id
        ).delete()
        self.db.flush()
    
    def create_criterion(
        self,
        story_id: int,
        criterion_text: str,
        display_order: int
    ) -> AcceptanceCriterion:
        """Create a new acceptance criterion.
        
        Args:
            story_id: Story ID
            criterion_text: Criterion text
            display_order: Display order position
            
        Returns:
            Created AcceptanceCriterion instance
        """
        criterion = AcceptanceCriterion(
            story_id=story_id,
            criterion_text=criterion_text,
            display_order=display_order
        )
        self.db.add(criterion)
        self.db.flush()
        return criterion

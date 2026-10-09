"""Readiness service for rule evaluation and gap identification."""
import json

from sqlalchemy.orm import Session

from app.domain.readiness_rules import evaluate_readiness
from app.models.workspace import Workspace
from app.repositories.workspace_repository import WorkspaceRepository


class ReadinessService:
    """Service for readiness evaluation."""
    
    def __init__(self, db: Session):
        """Initialize service with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
        self.workspace_repo = WorkspaceRepository(db)
    
    def evaluate_readiness(self, workspace: Workspace) -> dict:
        """Evaluate workspace readiness and generate summary.
        
        Implements readiness computation per LLD Section 6.2.
        
        Args:
            workspace: Workspace instance with eager-loaded relationships
            
        Returns:
            Dictionary with readiness status, summary, gaps, and interpretation
        """
        # Delegate to domain rules
        status, gaps = evaluate_readiness(workspace)
        
        # Build summary statistics
        business_goals = json.loads(workspace.business_goals_json)
        
        stories_with_criteria = 0
        stories_with_priority = 0
        
        for story in workspace.stories:
            if story.acceptance_criteria and len(story.acceptance_criteria) > 0:
                stories_with_criteria += 1
            if story.priority:
                stories_with_priority += 1
        
        summary = {
            "visionComplete": self._is_vision_complete(workspace),
            "businessGoalsCount": len(business_goals),
            "storyCount": len(workspace.stories) if workspace.stories else 0,
            "storiesWithAcceptanceCriteria": stories_with_criteria,
            "storiesWithPriority": stories_with_priority,
            "reviewNotesCount": len(workspace.review_notes) if workspace.review_notes else 0
        }
        
        # Update workspace status based on readiness
        if workspace.status != status.value:
            self.workspace_repo.update_status(workspace, status.value)
            self.db.commit()
        
        return {
            "workspaceId": workspace.id,
            "status": status.value,
            "summary": summary,
            "gaps": gaps,
            "releaseReadinessInterpretation": (
                "All included stories must have acceptance criteria and assigned priorities "
                "before review-ready interpretation is met."
            )
        }
    
    def _is_vision_complete(self, workspace: Workspace) -> bool:
        """Check if vision section is complete.
        
        Args:
            workspace: Workspace instance
            
        Returns:
            True if vision section has all required fields
        """
        if not workspace.vision_statement or not workspace.target_problem:
            return False
        
        business_goals = json.loads(workspace.business_goals_json)
        if len(business_goals) < 1:
            return False
        
        success_measures = json.loads(workspace.success_measures_json)
        return not len(success_measures) < 1

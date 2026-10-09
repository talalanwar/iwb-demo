"""Unit tests for story_service.py."""
import pytest
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.models.story import Story
from app.models.acceptance_criterion import AcceptanceCriterion
from app.services.story_service import StoryService


class TestStoryService:
    """Test suite for StoryService."""
    
    def test_upsert_story_set_create_new_stories(self, test_db: Session, test_workspace: Workspace):
        """Test creating new stories via upsert."""
        service = StoryService(test_db)
        
        stories_data = [
            {
                "title": "New Story 1",
                "actor": "User",
                "need": "to create stories",
                "outcome": "stories are created",
                "description": "Test description",
                "priority": "HIGH",
                "backlogOrder": 1,
                "acceptanceCriteria": [
                    {"text": "Criterion 1"},
                    {"text": "Criterion 2"}
                ]
            },
            {
                "title": "New Story 2",
                "actor": "Admin",
                "need": "to manage stories",
                "outcome": "stories are managed",
                "priority": "MEDIUM",
                "backlogOrder": 2,
                "acceptanceCriteria": [
                    {"text": "Criterion A"}
                ]
            }
        ]
        
        count, validation = service.upsert_story_set(test_workspace, stories_data)
        
        assert count == 2
        assert validation["storiesMissingPriority"] == 0
        assert validation["storiesMissingAcceptanceCriteria"] == 0
        
        # Verify stories were created
        stories = service.get_ordered_backlog(test_workspace.id)
        assert len(stories) == 2
        assert stories[0].title == "New Story 1"
        assert stories[0].backlog_order == 1
        assert len(stories[0].acceptance_criteria) == 2
    
    def test_upsert_story_set_update_existing(self, test_db: Session, test_workspace: Workspace, test_story: Story):
        """Test updating existing stories via upsert."""
        service = StoryService(test_db)
        
        stories_data = [
            {
                "id": test_story.id,
                "title": "Updated Story",
                "actor": "Updated Actor",
                "need": "updated need",
                "outcome": "updated outcome",
                "description": "Updated description",
                "priority": "LOW",
                "backlogOrder": 1,
                "acceptanceCriteria": [
                    {"text": "Updated Criterion"}
                ]
            }
        ]
        
        count, validation = service.upsert_story_set(test_workspace, stories_data)
        
        assert count == 1
        
        # Verify story was updated
        test_db.refresh(test_story)
        assert test_story.title == "Updated Story"
        assert test_story.actor == "Updated Actor"
        assert test_story.priority == "LOW"
        assert len(test_story.acceptance_criteria) == 1
    
    def test_upsert_story_set_delete_omitted(self, test_db: Session, test_workspace: Workspace):
        """Test that omitted stories are deleted."""
        # Create initial stories
        story1 = Story(
            workspace_id=test_workspace.id,
            title="Story 1",
            actor="User",
            need_text="need 1",
            outcome_text="outcome 1",
            backlog_order=1
        )
        story2 = Story(
            workspace_id=test_workspace.id,
            title="Story 2",
            actor="User",
            need_text="need 2",
            outcome_text="outcome 2",
            backlog_order=2
        )
        test_db.add_all([story1, story2])
        test_db.commit()
        
        service = StoryService(test_db)
        
        # Upsert with only story1 - story2 should be deleted
        stories_data = [
            {
                "id": story1.id,
                "title": "Story 1 Updated",
                "actor": "User",
                "need": "need 1",
                "outcome": "outcome 1",
                "backlogOrder": 1,
                "acceptanceCriteria": []
            }
        ]
        
        service.upsert_story_set(test_workspace, stories_data)
        
        # Verify only story1 remains
        stories = service.get_ordered_backlog(test_workspace.id)
        assert len(stories) == 1
        assert stories[0].id == story1.id
    
    def test_upsert_story_set_validation_summary(self, test_db: Session, test_workspace: Workspace):
        """Test validation summary for incomplete stories."""
        service = StoryService(test_db)
        
        stories_data = [
            {
                "title": "Story With Priority No Criteria",
                "actor": "User",
                "need": "need",
                "outcome": "outcome",
                "priority": "HIGH",
                "backlogOrder": 1,
                "acceptanceCriteria": []  # Missing criteria
            },
            {
                "title": "Story With Criteria No Priority",
                "actor": "User",
                "need": "need",
                "outcome": "outcome",
                "priority": None,  # Missing priority
                "backlogOrder": 2,
                "acceptanceCriteria": [{"text": "Criterion"}]
            },
            {
                "title": "Complete Story",
                "actor": "User",
                "need": "need",
                "outcome": "outcome",
                "priority": "MEDIUM",
                "backlogOrder": 3,
                "acceptanceCriteria": [{"text": "Criterion"}]
            }
        ]
        
        count, validation = service.upsert_story_set(test_workspace, stories_data)
        
        assert count == 3
        assert validation["storiesMissingPriority"] == 1
        assert validation["storiesMissingAcceptanceCriteria"] == 1
    
    def test_upsert_story_set_acceptance_criteria_order(self, test_db: Session, test_workspace: Workspace):
        """Test that acceptance criteria maintain display order."""
        service = StoryService(test_db)
        
        stories_data = [
            {
                "title": "Story With Ordered Criteria",
                "actor": "User",
                "need": "need",
                "outcome": "outcome",
                "priority": "HIGH",
                "backlogOrder": 1,
                "acceptanceCriteria": [
                    {"text": "First Criterion"},
                    {"text": "Second Criterion"},
                    {"text": "Third Criterion"}
                ]
            }
        ]
        
        service.upsert_story_set(test_workspace, stories_data)
        
        stories = service.get_ordered_backlog(test_workspace.id)
        assert len(stories) == 1
        
        criteria = stories[0].acceptance_criteria
        assert len(criteria) == 3
        assert criteria[0].display_order == 1
        assert criteria[0].criterion_text == "First Criterion"
        assert criteria[1].display_order == 2
        assert criteria[2].display_order == 3
    
    def test_upsert_story_set_max_20_stories(self, test_db: Session, test_workspace: Workspace):
        """Test that story set respects 20-story limit per LLD."""
        service = StoryService(test_db)
        
        # Create 20 stories (max allowed)
        stories_data = [
            {
                "title": f"Story {i}",
                "actor": "User",
                "need": "need",
                "outcome": "outcome",
                "priority": "MEDIUM",
                "backlogOrder": i + 1,
                "acceptanceCriteria": []
            }
            for i in range(20)
        ]
        
        count, _ = service.upsert_story_set(test_workspace, stories_data)
        assert count == 20
        
        stories = service.get_ordered_backlog(test_workspace.id)
        assert len(stories) == 20
    
    def test_get_ordered_backlog(self, test_db: Session, test_workspace: Workspace):
        """Test retrieving stories ordered by backlog_order."""
        service = StoryService(test_db)
        
        # Create stories out of order
        story3 = Story(
            workspace_id=test_workspace.id,
            title="Story 3",
            actor="User",
            need_text="need",
            outcome_text="outcome",
            backlog_order=3
        )
        story1 = Story(
            workspace_id=test_workspace.id,
            title="Story 1",
            actor="User",
            need_text="need",
            outcome_text="outcome",
            backlog_order=1
        )
        story2 = Story(
            workspace_id=test_workspace.id,
            title="Story 2",
            actor="User",
            need_text="need",
            outcome_text="outcome",
            backlog_order=2
        )
        test_db.add_all([story3, story1, story2])
        test_db.commit()
        
        # Get ordered backlog
        stories = service.get_ordered_backlog(test_workspace.id)
        
        assert len(stories) == 3
        assert stories[0].title == "Story 1"
        assert stories[1].title == "Story 2"
        assert stories[2].title == "Story 3"
    
    def test_upsert_story_set_updates_workspace_status(self, test_db: Session, test_workspace: Workspace):
        """Test that upsert updates workspace status."""
        # Set workspace to EMPTY status
        test_workspace.status = "EMPTY"
        test_db.commit()
        
        service = StoryService(test_db)
        
        stories_data = [
            {
                "title": "First Story",
                "actor": "User",
                "need": "need",
                "outcome": "outcome",
                "backlogOrder": 1,
                "acceptanceCriteria": []
            }
        ]
        
        service.upsert_story_set(test_workspace, stories_data)
        
        # Verify workspace status updated
        test_db.refresh(test_workspace)
        assert test_workspace.status == "DRAFTING_BACKLOG"
    
    def test_upsert_story_set_replaces_criteria(self, test_db: Session, test_workspace: Workspace):
        """Test that updating story replaces existing criteria."""
        service = StoryService(test_db)
        
        # Create story with initial criteria
        stories_data = [
            {
                "title": "Story",
                "actor": "User",
                "need": "need",
                "outcome": "outcome",
                "backlogOrder": 1,
                "acceptanceCriteria": [
                    {"text": "Old Criterion 1"},
                    {"text": "Old Criterion 2"}
                ]
            }
        ]
        
        service.upsert_story_set(test_workspace, stories_data)
        stories = service.get_ordered_backlog(test_workspace.id)
        story_id = stories[0].id
        
        # Update with new criteria
        stories_data = [
            {
                "id": story_id,
                "title": "Story",
                "actor": "User",
                "need": "need",
                "outcome": "outcome",
                "backlogOrder": 1,
                "acceptanceCriteria": [
                    {"text": "New Criterion"}
                ]
            }
        ]
        
        service.upsert_story_set(test_workspace, stories_data)
        
        # Verify old criteria replaced
        stories = service.get_ordered_backlog(test_workspace.id)
        assert len(stories[0].acceptance_criteria) == 1
        assert stories[0].acceptance_criteria[0].criterion_text == "New Criterion"

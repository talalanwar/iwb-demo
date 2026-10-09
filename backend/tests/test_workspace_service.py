"""Unit tests for workspace_service.py."""
import json
import pytest
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workspace import Workspace
from app.models.story import Story
from app.models.acceptance_criterion import AcceptanceCriterion
from app.services.workspace_service import WorkspaceService


class TestWorkspaceService:
    """Test suite for WorkspaceService."""
    
    def test_create_workspace_for_new_user(self, test_db: Session, test_user: User):
        """Test creating workspace for user without existing workspace."""
        service = WorkspaceService(test_db)
        
        # Create workspace
        workspace = service.create_or_open_workspace(test_user.id)
        
        assert workspace is not None
        assert workspace.owner_user_id == test_user.id
        assert workspace.product_name == "Untitled Product"
        assert workspace.id is not None
    
    def test_open_existing_workspace(self, test_db: Session, test_workspace: Workspace):
        """Test opening existing workspace."""
        service = WorkspaceService(test_db)
        
        # Open existing workspace
        workspace = service.create_or_open_workspace(test_workspace.owner_user_id)
        
        assert workspace is not None
        assert workspace.id == test_workspace.id
        assert workspace.product_name == test_workspace.product_name
    
    def test_one_workspace_per_user(self, test_db: Session, test_user: User):
        """Test that only one workspace is created per user."""
        service = WorkspaceService(test_db)
        
        # Create first workspace
        workspace1 = service.create_or_open_workspace(test_user.id)
        workspace1_id = workspace1.id
        
        # Attempt to create again - should return same workspace
        workspace2 = service.create_or_open_workspace(test_user.id)
        
        assert workspace1.id == workspace2.id
        assert workspace1_id == workspace2.id
    
    def test_assemble_workspace_aggregate_minimal(self, test_db: Session, test_workspace: Workspace):
        """Test assembling workspace aggregate with minimal data."""
        service = WorkspaceService(test_db)
        
        # Assemble aggregate
        aggregate = service.assemble_workspace_aggregate(test_workspace)
        
        assert aggregate is not None
        assert aggregate["id"] == test_workspace.id
        assert aggregate["productName"] == test_workspace.product_name
        assert aggregate["shortDescription"] == test_workspace.short_description
        assert "vision" in aggregate
        assert "stories" in aggregate
        assert "review" in aggregate
    
    def test_assemble_workspace_aggregate_vision(self, test_db: Session, test_workspace: Workspace):
        """Test vision section in workspace aggregate."""
        service = WorkspaceService(test_db)
        
        # Assemble aggregate
        aggregate = service.assemble_workspace_aggregate(test_workspace)
        
        vision = aggregate["vision"]
        assert vision["visionStatement"] == "Test vision"
        assert vision["targetProblem"] == "Test problem"
        assert len(vision["businessGoals"]) == 2
        assert "Goal 1" in vision["businessGoals"]
        assert len(vision["successMeasures"]) == 2
        assert "Measure 1" in vision["successMeasures"]
    
    def test_assemble_workspace_aggregate_with_stories(
        self, test_db: Session, test_workspace: Workspace
    ):
        """Test workspace aggregate with stories and criteria."""
        # Add story with criteria
        story = Story(
            workspace_id=test_workspace.id,
            title="Test Story",
            actor="User",
            need_text="to test",
            outcome_text="test works",
            priority="HIGH",
            backlog_order=1
        )
        test_db.add(story)
        test_db.commit()
        test_db.refresh(story)
        
        criterion = AcceptanceCriterion(
            story_id=story.id,
            criterion_text="Test criterion",
            display_order=1
        )
        test_db.add(criterion)
        test_db.commit()
        
        # Refresh workspace to load relationships
        test_db.refresh(test_workspace)
        
        service = WorkspaceService(test_db)
        aggregate = service.assemble_workspace_aggregate(test_workspace)
        
        assert len(aggregate["stories"]) == 1
        story_data = aggregate["stories"][0]
        assert story_data["title"] == "Test Story"
        assert story_data["priority"] == "HIGH"
        assert len(story_data["acceptanceCriteria"]) == 1
        assert story_data["acceptanceCriteria"][0]["text"] == "Test criterion"
    
    def test_update_workspace_metadata(self, test_db: Session, test_workspace: Workspace):
        """Test updating workspace metadata."""
        service = WorkspaceService(test_db)
        
        # Update metadata
        updated = service.update_workspace_metadata_and_vision(
            workspace=test_workspace,
            product_name="Updated Product Name",
            short_description="Updated description"
        )
        
        assert updated.product_name == "Updated Product Name"
        assert updated.short_description == "Updated description"
    
    def test_update_workspace_vision(self, test_db: Session, test_workspace: Workspace):
        """Test updating workspace vision fields."""
        service = WorkspaceService(test_db)
        
        # Update vision
        updated = service.update_workspace_metadata_and_vision(
            workspace=test_workspace,
            vision_statement="New vision",
            target_problem="New problem",
            business_goals=["New Goal 1", "New Goal 2", "New Goal 3"],
            success_measures=["New Measure 1"]
        )
        
        assert updated.vision_statement == "New vision"
        assert updated.target_problem == "New problem"
        
        goals = json.loads(updated.business_goals_json)
        assert len(goals) == 3
        assert "New Goal 1" in goals
        
        measures = json.loads(updated.success_measures_json)
        assert len(measures) == 1
        assert "New Measure 1" in measures
    
    def test_assemble_workspace_aggregate_review_section(
        self, test_db: Session, test_workspace: Workspace
    ):
        """Test review section in workspace aggregate."""
        from app.models.review_share import ReviewShare
        from app.models.review_note import ReviewNote
        from datetime import datetime, UTC, timedelta
        
        # Add review share
        share = ReviewShare(
            workspace_id=test_workspace.id,
            share_token="test-token-123",
            requires_auth=True,
            created_by_user_id=test_workspace.owner_user_id,
            expires_at=datetime.now(UTC) + timedelta(days=30)
        )
        test_db.add(share)
        test_db.commit()
        
        # Add review note
        note = ReviewNote(
            workspace_id=test_workspace.id,
            reviewer_name="Test Reviewer",
            note_text="Great work!"
        )
        test_db.add(note)
        test_db.commit()
        
        # Refresh workspace
        test_db.refresh(test_workspace)
        
        service = WorkspaceService(test_db)
        aggregate = service.assemble_workspace_aggregate(test_workspace)
        
        review = aggregate["review"]
        assert review["shareToken"] == "test-token-123"
        assert len(review["notes"]) == 1
        assert review["notes"][0]["reviewerName"] == "Test Reviewer"
        assert review["notes"][0]["noteText"] == "Great work!"

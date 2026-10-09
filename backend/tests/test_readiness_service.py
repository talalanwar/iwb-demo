"""Unit tests for readiness_service.py."""
import json
import pytest
from sqlalchemy.orm import Session

from app.models.workspace import Workspace
from app.models.story import Story
from app.models.acceptance_criterion import AcceptanceCriterion
from app.services.readiness_service import ReadinessService


class TestReadinessService:
    """Test suite for ReadinessService."""
    
    def test_evaluate_readiness_not_started(self, test_db: Session):
        """Test readiness evaluation for empty workspace."""
        from app.models.user import User
        
        # Create user and empty workspace
        user = User(
            email="empty@example.com",
            password_hash="hash",
            display_name="Empty User"
        )
        test_db.add(user)
        test_db.commit()
        
        workspace = Workspace(
            owner_user_id=user.id,
            product_name="Empty Product",
            business_goals_json='[]',
            success_measures_json='[]',
            status="EMPTY"
        )
        test_db.add(workspace)
        test_db.commit()
        test_db.refresh(workspace)
        
        service = ReadinessService(test_db)
        result = service.evaluate_readiness(workspace)
        
        assert result["status"] == "NOT_STARTED"
        assert result["workspaceId"] == workspace.id
        assert "summary" in result
        assert "gaps" in result
    
    def test_evaluate_readiness_in_progress(self, test_db: Session, test_workspace: Workspace):
        """Test readiness evaluation for workspace in progress."""
        # Set incomplete vision - missing target problem should generate gap
        test_workspace.vision_statement = "Test vision"
        test_workspace.target_problem = None  # Missing target problem
        test_db.commit()
        
        # Add a story to ensure we're not in NOT_STARTED status
        story = Story(
            workspace_id=test_workspace.id,
            title="In Progress Story",
            actor="User",
            need_text="to test",
            outcome_text="test works",
            backlog_order=1
        )
        test_db.add(story)
        test_db.commit()
        test_db.refresh(test_workspace)
        
        service = ReadinessService(test_db)
        result = service.evaluate_readiness(test_workspace)
        
        # Should be IN_PROGRESS due to incomplete vision
        assert result["status"] in ["IN_PROGRESS", "NEEDS_ATTENTION"]
        # Should have gap for missing target problem
        gap_codes = [g["code"] for g in result["gaps"]]
        assert "MISSING_TARGET_PROBLEM" in gap_codes
    
    def test_evaluate_readiness_needs_attention(self, test_db: Session, test_workspace: Workspace):
        """Test readiness evaluation with missing criteria or priority."""
        # Add story without acceptance criteria
        story = Story(
            workspace_id=test_workspace.id,
            title="Incomplete Story",
            actor="User",
            need_text="to test",
            outcome_text="test works",
            priority=None,  # Missing priority
            backlog_order=1
        )
        test_db.add(story)
        test_db.commit()
        test_db.refresh(test_workspace)
        
        service = ReadinessService(test_db)
        result = service.evaluate_readiness(test_workspace)
        
        assert result["status"] in ["IN_PROGRESS", "NEEDS_ATTENTION"]
        assert result["summary"]["storyCount"] == 1
        assert result["summary"]["storiesWithAcceptanceCriteria"] == 0
        assert result["summary"]["storiesWithPriority"] == 0
    
    def test_evaluate_readiness_ready_for_review(self, test_db: Session, test_workspace: Workspace):
        """Test readiness evaluation for complete workspace."""
        # Ensure vision is complete
        test_workspace.vision_statement = "Complete vision"
        test_workspace.target_problem = "Problem statement"
        test_workspace.business_goals_json = '["Goal 1", "Goal 2"]'
        test_workspace.success_measures_json = '["Measure 1"]'
        
        # Add complete story with criteria and priority
        story = Story(
            workspace_id=test_workspace.id,
            title="Complete Story",
            actor="User",
            need_text="to test",
            outcome_text="test works",
            priority="HIGH",
            backlog_order=1
        )
        test_db.add(story)
        test_db.commit()
        
        criterion = AcceptanceCriterion(
            story_id=story.id,
            criterion_text="Test criterion",
            display_order=1
        )
        test_db.add(criterion)
        test_db.commit()
        test_db.refresh(test_workspace)
        
        service = ReadinessService(test_db)
        result = service.evaluate_readiness(test_workspace)
        
        assert result["status"] == "READY_FOR_REVIEW"
        assert result["summary"]["visionComplete"] is True
        assert result["summary"]["storyCount"] == 1
        assert result["summary"]["storiesWithAcceptanceCriteria"] == 1
        assert result["summary"]["storiesWithPriority"] == 1
        assert len(result["gaps"]) == 0
    
    def test_gap_detection_missing_criteria(self, test_db: Session, test_workspace: Workspace):
        """Test gap detection for missing acceptance criteria."""
        # Add story without criteria
        story = Story(
            workspace_id=test_workspace.id,
            title="Story Without Criteria",
            actor="User",
            need_text="to test",
            outcome_text="test works",
            priority="MEDIUM",
            backlog_order=1
        )
        test_db.add(story)
        test_db.commit()
        test_db.refresh(test_workspace)
        
        service = ReadinessService(test_db)
        result = service.evaluate_readiness(test_workspace)
        
        # Check for missing criteria gap
        gaps = result["gaps"]
        criteria_gaps = [g for g in gaps if g["code"] == "MISSING_ACCEPTANCE_CRITERIA"]
        assert len(criteria_gaps) > 0
        assert "navigateTo" in criteria_gaps[0]
    
    def test_gap_detection_missing_priority(self, test_db: Session, test_workspace: Workspace):
        """Test gap detection for missing priority."""
        # Add story without priority but with criteria
        story = Story(
            workspace_id=test_workspace.id,
            title="Story Without Priority",
            actor="User",
            need_text="to test",
            outcome_text="test works",
            priority=None,
            backlog_order=1
        )
        test_db.add(story)
        test_db.commit()
        
        criterion = AcceptanceCriterion(
            story_id=story.id,
            criterion_text="Test criterion",
            display_order=1
        )
        test_db.add(criterion)
        test_db.commit()
        test_db.refresh(test_workspace)
        
        service = ReadinessService(test_db)
        result = service.evaluate_readiness(test_workspace)
        
        # Check for missing priority gap
        gaps = result["gaps"]
        priority_gaps = [g for g in gaps if g["code"] == "MISSING_PRIORITY"]
        assert len(priority_gaps) > 0
    
    def test_status_determination_updates_workspace(self, test_db: Session, test_workspace: Workspace):
        """Test that readiness evaluation updates workspace status."""
        original_status = test_workspace.status
        
        service = ReadinessService(test_db)
        result = service.evaluate_readiness(test_workspace)
        
        # Refresh workspace to get updated status
        test_db.refresh(test_workspace)
        
        # Status should match result
        assert test_workspace.status == result["status"]
    
    def test_vision_completeness_check(self, test_db: Session, test_workspace: Workspace):
        """Test vision completeness logic."""
        service = ReadinessService(test_db)
        
        # Complete vision
        test_workspace.vision_statement = "Vision"
        test_workspace.target_problem = "Problem"
        test_workspace.business_goals_json = '["Goal 1"]'
        test_workspace.success_measures_json = '["Measure 1"]'
        test_db.commit()
        test_db.refresh(test_workspace)
        
        result = service.evaluate_readiness(test_workspace)
        assert result["summary"]["visionComplete"] is True
        
        # Incomplete vision - missing target problem
        test_workspace.target_problem = None
        test_db.commit()
        test_db.refresh(test_workspace)
        
        result = service.evaluate_readiness(test_workspace)
        assert result["summary"]["visionComplete"] is False
    
    def test_summary_statistics(self, test_db: Session, test_workspace: Workspace):
        """Test summary statistics calculation."""
        from app.models.review_note import ReviewNote
        
        # Add multiple stories
        for i in range(3):
            story = Story(
                workspace_id=test_workspace.id,
                title=f"Story {i}",
                actor="User",
                need_text="to test",
                outcome_text="test works",
                priority="HIGH" if i < 2 else None,
                backlog_order=i + 1
            )
            test_db.add(story)
            test_db.commit()
            
            if i < 1:
                criterion = AcceptanceCriterion(
                    story_id=story.id,
                    criterion_text=f"Criterion {i}",
                    display_order=1
                )
                test_db.add(criterion)
        
        # Add review note
        note = ReviewNote(
            workspace_id=test_workspace.id,
            reviewer_name="Reviewer",
            note_text="Note"
        )
        test_db.add(note)
        test_db.commit()
        test_db.refresh(test_workspace)
        
        service = ReadinessService(test_db)
        result = service.evaluate_readiness(test_workspace)
        
        summary = result["summary"]
        assert summary["storyCount"] == 3
        assert summary["storiesWithAcceptanceCriteria"] == 1
        assert summary["storiesWithPriority"] == 2
        assert summary["reviewNotesCount"] == 1
        assert summary["businessGoalsCount"] == 2  # From fixture

"""Readiness evaluation rules per LLD Section 6.2."""
import json
from enum import Enum


class ReadinessStatus(str, Enum):
    """Readiness status enumeration per LLD Section 6.2."""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    NEEDS_ATTENTION = "NEEDS_ATTENTION"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"


class GapCode(str, Enum):
    """Gap code enumeration for readiness gaps."""
    MISSING_ACCEPTANCE_CRITERIA = "MISSING_ACCEPTANCE_CRITERIA"
    MISSING_PRIORITY = "MISSING_PRIORITY"
    INVALID_BACKLOG_ORDER = "INVALID_BACKLOG_ORDER"


def evaluate_readiness(workspace) -> tuple[ReadinessStatus, list[dict]]:
    """Evaluate workspace readiness and identify gaps.
    
    Implements binding business rules from FR-06, FR-09, and Release Readiness Interpretation.
    
    Args:
        workspace: Workspace model instance with stories and criteria relationships
        
    Returns:
        Tuple of (ReadinessStatus, list of gap dictionaries)
        Gap dictionaries contain: code, message, navigateTo
    """
    gaps = []
    
    # Check vision completeness
    vision_complete = _is_vision_complete(workspace)
    
    # Check story count
    story_count = len(workspace.stories) if workspace.stories else 0
    
    # Determine status based on overall state
    if not vision_complete and story_count == 0:
        return ReadinessStatus.NOT_STARTED, gaps
    
    # Check each story for completeness
    stories_with_criteria = 0
    stories_with_priority = 0
    backlog_orders_seen = set()
    
    for story in workspace.stories:
        # Check acceptance criteria
        criteria_count = len(story.acceptance_criteria) if story.acceptance_criteria else 0
        if criteria_count == 0:
            gaps.append({
                "code": GapCode.MISSING_ACCEPTANCE_CRITERIA,
                "message": f"Story '{story.title}' does not have acceptance criteria.",
                "navigateTo": f"/backlog?storyId={story.id}&focus=criteria"
            })
        else:
            stories_with_criteria += 1
        
        # Check priority
        if not story.priority:
            gaps.append({
                "code": GapCode.MISSING_PRIORITY,
                "message": f"Story '{story.title}' does not have a priority.",
                "navigateTo": f"/backlog?storyId={story.id}&focus=priority"
            })
        else:
            stories_with_priority += 1
        
        # Check backlog order uniqueness
        if story.backlog_order in backlog_orders_seen:
            gaps.append({
                "code": GapCode.INVALID_BACKLOG_ORDER,
                "message": f"Story '{story.title}' has duplicate backlog order {story.backlog_order}.",
                "navigateTo": f"/backlog?storyId={story.id}"
            })
        backlog_orders_seen.add(story.backlog_order)
    
    # Add vision gaps if incomplete
    if not vision_complete:
        if not workspace.vision_statement:
            gaps.append({
                "code": "MISSING_VISION_STATEMENT",
                "message": "Vision statement is required for readiness completeness.",
                "navigateTo": "/workspace#vision"
            })
        if not workspace.target_problem:
            gaps.append({
                "code": "MISSING_TARGET_PROBLEM",
                "message": "Target problem is required for readiness completeness.",
                "navigateTo": "/workspace#vision"
            })
        
        # Check business goals
        business_goals = json.loads(workspace.business_goals_json)
        if len(business_goals) < 1:
            gaps.append({
                "code": "MISSING_BUSINESS_GOALS",
                "message": "At least one business goal is required for readiness completeness.",
                "navigateTo": "/workspace#business-context"
            })
        
        # Check success measures
        success_measures = json.loads(workspace.success_measures_json)
        if len(success_measures) < 1:
            gaps.append({
                "code": "MISSING_SUCCESS_MEASURES",
                "message": "At least one success measure is required for readiness completeness.",
                "navigateTo": "/workspace#business-context"
            })
    
    # Determine final status
    if not gaps:
        return ReadinessStatus.READY_FOR_REVIEW, gaps
    
    # If vision complete and stories exist but gaps remain
    if vision_complete and story_count > 0:
        return ReadinessStatus.NEEDS_ATTENTION, gaps
    
    # Otherwise still in progress
    return ReadinessStatus.IN_PROGRESS, gaps


def _is_vision_complete(workspace) -> bool:
    """Check if vision section is complete.
    
    Args:
        workspace: Workspace model instance
        
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

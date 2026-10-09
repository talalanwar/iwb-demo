"""
Idempotent seed data script for Product Learning Studio.

Creates default demo user and realistic sample data for all tables.
Safe to run multiple times - checks existence before inserting.
Called from main.py lifespan hook on startup.
"""
import json
import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.domain.share_access import generate_share_token
from app.models.acceptance_criterion import AcceptanceCriterion
from app.models.review_note import ReviewNote
from app.models.review_share import ReviewShare
from app.models.story import Story
from app.models.user import User
from app.models.workspace import Workspace

logger = logging.getLogger(__name__)

# Default demo credentials - MUST match frontend login defaults and README
DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "demo1234"
DEMO_DISPLAY_NAME = "Demo User"


def seed_data(db: Session) -> None:
    """
    Seed database with default demo user and sample data.
    
    Idempotent - checks existence before inserting.
    Creates:
    - Default demo user (id=1, email: demo@example.com, password: demo123)
    - One complete workspace with product name, vision, business context
    - 3 sample stories with acceptance criteria and priorities
    - One review share token
    - One review note
    
    Args:
        db: SQLAlchemy database session
    """
    logger.info("Starting seed data initialization...")
    
    try:
        # Check if demo user already exists
        existing_user = db.query(User).filter(User.email == DEMO_EMAIL).first()
        
        if existing_user:
            logger.info(f"Demo user already exists: {DEMO_EMAIL}")
            demo_user = existing_user
        else:
            # Create demo user with id=1
            logger.info(f"Creating demo user: {DEMO_EMAIL}")
            demo_user = User(
                id=1,
                email=DEMO_EMAIL,
                password_hash=get_password_hash(DEMO_PASSWORD),
                display_name=DEMO_DISPLAY_NAME,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                deleted_at=None
            )
            db.add(demo_user)
            db.flush()  # Ensure user.id is available
            logger.info(f"Demo user created with id={demo_user.id}")
        
        # Check if workspace already exists for demo user
        existing_workspace = db.query(Workspace).filter(
            Workspace.owner_user_id == demo_user.id
        ).first()
        
        if existing_workspace:
            logger.info(f"Demo workspace already exists: id={existing_workspace.id}")
            workspace = existing_workspace
        else:
            # Create demo workspace with complete product definition
            logger.info("Creating demo workspace with product definition...")
            
            business_goals = [
                "Enable aspiring product teams to learn IBM Product Workbench concepts through hands-on practice",
                "Reduce time to create a reviewable product definition from days to under 15 minutes",
                "Provide clear guidance at each step to avoid blank-page syndrome",
                "Generate structured, shareable product specifications that reviewers can easily evaluate",
                "Support iterative refinement with readiness feedback and navigable gap detection"
            ]
            
            success_measures = [
                "80%+ of first-time users complete a full product definition in under 15 minutes",
                "90%+ of reviewed sessions result in clear product scope understanding",
                "Readiness score improves by at least 30 points after addressing guided prompts",
                "Review turnaround time reduced by 50% compared to unstructured drafts",
                "User satisfaction rating of 4.5/5 or higher for onboarding clarity"
            ]
            
            workspace = Workspace(
                owner_user_id=demo_user.id,
                product_name="Product Learning Studio",
                short_description="A browser-based demo SaaS that helps product learners turn rough ideas into structured, reviewable product definitions",
                vision_statement="Empower aspiring product teams to confidently learn and apply IBM Product Workbench principles by transforming early-stage product thinking into clear, actionable specifications through guided workflows and immediate feedback.",
                target_problem="Product learners face blank-page syndrome when starting product definitions, struggle to determine appropriate MVP scope, and produce vague specifications that reviewers cannot easily evaluate or act upon.",
                business_goals_json=json.dumps(business_goals),
                success_measures_json=json.dumps(success_measures),
                status="READY_FOR_REVIEW",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(workspace)
            db.flush()
            logger.info(f"Demo workspace created: id={workspace.id}")
        
        # Check if stories already exist for this workspace
        existing_stories = db.query(Story).filter(
            Story.workspace_id == workspace.id
        ).count()
        
        if existing_stories > 0:
            logger.info(f"Demo stories already exist: count={existing_stories}")
        else:
            # Create 3 sample stories with acceptance criteria
            logger.info("Creating 3 sample stories with acceptance criteria...")
            
            # Story 1: User Sign-In
            story1 = Story(
                workspace_id=workspace.id,
                title="User Sign-In",
                actor="Product Learner",
                need_text="sign in to my personal workspace",
                outcome_text="I can securely access my saved product definitions and continue working where I left off",
                description="Enable authenticated access to personal workspace with email and password credentials",
                priority="HIGH",
                backlog_order=1,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(story1)
            db.flush()
            
            criteria1 = [
                AcceptanceCriterion(
                    story_id=story1.id,
                    criterion_text="Login form accepts email and password inputs",
                    display_order=1,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story1.id,
                    criterion_text="Valid credentials return auth token and redirect to workspace",
                    display_order=2,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story1.id,
                    criterion_text="Invalid credentials display clear error message without exposing security details",
                    display_order=3,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story1.id,
                    criterion_text="Password is masked during input and transmitted securely",
                    display_order=4,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
            ]
            db.add_all(criteria1)
            logger.info(f"Story 1 created: {story1.title} with {len(criteria1)} criteria")
            
            # Story 2: Define Product Vision
            story2 = Story(
                workspace_id=workspace.id,
                title="Define Product Vision",
                actor="Product Learner",
                need_text="capture and edit my product vision, target problem, business goals, and success measures",
                outcome_text="I have a clear, structured vision section that guides my requirements and helps reviewers understand my product intent",
                description="Provide guided forms for vision statement, target problem, business goals array (max 5), and success measures array (max 5)",
                priority="HIGH",
                backlog_order=2,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(story2)
            db.flush()
            
            criteria2 = [
                AcceptanceCriterion(
                    story_id=story2.id,
                    criterion_text="Vision section provides separate text areas for vision statement (max 1000 chars) and target problem (max 1000 chars)",
                    display_order=1,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story2.id,
                    criterion_text="Business goals can be added as a list with minimum 1 and maximum 5 items",
                    display_order=2,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story2.id,
                    criterion_text="Success measures can be added as a list with minimum 1 and maximum 5 items",
                    display_order=3,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story2.id,
                    criterion_text="Vision data persists on save and reloads on workspace reopen",
                    display_order=4,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story2.id,
                    criterion_text="Guided prompts display when fields are empty to reduce blank-page syndrome",
                    display_order=5,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
            ]
            db.add_all(criteria2)
            logger.info(f"Story 2 created: {story2.title} with {len(criteria2)} criteria")
            
            # Story 3: Prioritize Backlog Stories
            story3 = Story(
                workspace_id=workspace.id,
                title="Prioritize Backlog Stories",
                actor="Product Learner",
                need_text="assign priority levels and reorder stories in my backlog",
                outcome_text="I can communicate clear implementation priorities to reviewers and future teams, ensuring high-value work is tackled first",
                description="Enable drag-and-drop reordering of stories and priority assignment (HIGH, MEDIUM, LOW)",
                priority="MEDIUM",
                backlog_order=3,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(story3)
            db.flush()
            
            criteria3 = [
                AcceptanceCriterion(
                    story_id=story3.id,
                    criterion_text="Each story displays a priority selector with HIGH, MEDIUM, LOW options",
                    display_order=1,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story3.id,
                    criterion_text="Stories can be reordered via drag-and-drop or up/down controls",
                    display_order=2,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story3.id,
                    criterion_text="Backlog order persists on save and displays consistently on reopen",
                    display_order=3,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                AcceptanceCriterion(
                    story_id=story3.id,
                    criterion_text="Priority badges display with distinct colors (red for HIGH, yellow for MEDIUM, green for LOW)",
                    display_order=4,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
            ]
            db.add_all(criteria3)
            logger.info(f"Story 3 created: {story3.title} with {len(criteria3)} criteria")
        
        # Check if review share already exists for this workspace
        existing_share = db.query(ReviewShare).filter(
            ReviewShare.workspace_id == workspace.id
        ).first()
        
        if existing_share:
            logger.info(f"Demo review share already exists: token={existing_share.share_token[:8]}...")
            review_share = existing_share
        else:
            # Create review share token
            logger.info("Creating demo review share token...")
            review_share = ReviewShare(
                workspace_id=workspace.id,
                share_token=generate_share_token(),
                requires_auth=True,
                created_by_user_id=demo_user.id,
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            db.add(review_share)
            db.flush()
            logger.info(f"Review share created: token={review_share.share_token[:8]}...")
        
        # Check if review notes already exist for this workspace
        existing_notes = db.query(ReviewNote).filter(
            ReviewNote.workspace_id == workspace.id
        ).count()
        
        if existing_notes > 0:
            logger.info(f"Demo review notes already exist: count={existing_notes}")
        else:
            # Create sample review note
            logger.info("Creating demo review note...")
            review_note = ReviewNote(
                workspace_id=workspace.id,
                reviewer_name="Jane Reviewer",
                note_text="Great vision statement! The target problem is clear and compelling. Consider adding more specific success metrics with baseline and target values to make progress measurable. The story acceptance criteria are well-defined. Ready for implementation planning.",
                created_at=datetime.utcnow()
            )
            db.add(review_note)
            logger.info("Review note created")
        
        # Commit all changes
        db.commit()
        logger.info("Seed data initialization complete!")
        logger.info(f"Demo credentials: {DEMO_EMAIL} / {DEMO_PASSWORD}")
        
    except Exception as e:
        logger.error(f"Seed data initialization failed: {e}")
        db.rollback()
        raise

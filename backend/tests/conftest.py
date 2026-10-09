"""Pytest fixtures for backend unit tests."""
import logging
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from unittest.mock import MagicMock, patch

from app.core.database import Base
from app.models import (
    AcceptanceCriterion,
    ReviewNote,
    ReviewShare,
    Story,
    User,
    Workspace,
)


# Create a mock logger that accepts any arguments
mock_logger = MagicMock(spec=logging.Logger)


def mock_log_auth_event(*args, **kwargs):
    """Mock log_auth_event that accepts old signature without logger."""
    pass


def mock_log_save_event(*args, **kwargs):
    """Mock log_save_event that accepts old signature without logger."""
    pass


def mock_log_review_action(*args, **kwargs):
    """Mock log_review_action that accepts old signature without logger."""
    pass


def mock_log_authorization_failure(*args, **kwargs):
    """Mock log_authorization_failure that accepts old signature without logger."""
    pass


@pytest.fixture(autouse=True)
def mock_logging():
    """Mock logging functions to avoid parameter mismatch issues."""
    with patch('app.services.auth_service.log_auth_event', mock_log_auth_event), \
         patch('app.services.workspace_service.log_save_event', mock_log_save_event), \
         patch('app.services.story_service.log_save_event', mock_log_save_event), \
         patch('app.services.vision_service.log_save_event', mock_log_save_event), \
         patch('app.services.review_service.log_review_action', mock_log_review_action):
        yield


@pytest.fixture(scope="function")
def test_db():
    """Create in-memory SQLite database for testing."""
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Yield session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_user(test_db: Session):
    """Create test user fixture."""
    from app.core.security import get_password_hash
    
    user = User(
        id=1,
        email="test@example.com",
        password_hash=get_password_hash("testpass123"),
        display_name="Test User"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_workspace(test_db: Session, test_user: User):
    """Create test workspace fixture."""
    workspace = Workspace(
        id=1,
        owner_user_id=test_user.id,
        product_name="Test Product",
        short_description="Test description",
        vision_statement="Test vision",
        target_problem="Test problem",
        business_goals_json='["Goal 1", "Goal 2"]',
        success_measures_json='["Measure 1", "Measure 2"]',
        status="DRAFTING_BACKLOG"
    )
    test_db.add(workspace)
    test_db.commit()
    test_db.refresh(workspace)
    return workspace


@pytest.fixture(scope="function")
def test_story(test_db: Session, test_workspace: Workspace):
    """Create test story fixture."""
    story = Story(
        id=1,
        workspace_id=test_workspace.id,
        title="Test Story",
        actor="User",
        need_text="to test the system",
        outcome_text="the system works",
        description="Test story description",
        priority="HIGH",
        backlog_order=1
    )
    test_db.add(story)
    test_db.commit()
    test_db.refresh(story)
    return story

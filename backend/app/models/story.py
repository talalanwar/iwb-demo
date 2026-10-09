"""Story model for user stories with priority and ordering."""
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Story(Base):
    """User story with actor, need, outcome, priority, and backlog order.
    
    Stories belong to a workspace and contain acceptance criteria.
    Backlog order must be unique within a workspace.
    """
    __tablename__ = "stories"
    
    # Primary key as Integer
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Foreign key to workspaces.id with cascade delete
    workspace_id = Column(
        Integer, 
        ForeignKey("workspaces.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Story content fields
    title = Column(String(200), nullable=False)  # max 200 chars per LLD
    actor = Column(String(255), nullable=False)  # Required for recognizable story format
    need_text = Column(Text, nullable=False)     # Required for recognizable story format
    outcome_text = Column(Text, nullable=False)  # Required for recognizable story format
    description = Column(Text, nullable=True)
    
    # Priority and ordering
    priority = Column(String(20), nullable=True)  # HIGH, MEDIUM, LOW, or null during drafting
    backlog_order = Column(Integer, nullable=False)  # Positive integer, unique within workspace
    
    # Standard audit timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="stories")
    
    acceptance_criteria = relationship(
        "AcceptanceCriterion", 
        back_populates="story", 
        cascade="all, delete-orphan",
        order_by="AcceptanceCriterion.display_order"
    )
    
    # Unique constraint: one backlog_order per workspace
    __table_args__ = (
        UniqueConstraint("workspace_id", "backlog_order", name="uq_story_order"),
    )
    
    def __repr__(self):
        return f"<Story(id={self.id}, title='{self.title}', priority='{self.priority}', backlog_order={self.backlog_order})>"

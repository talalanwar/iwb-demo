"""Acceptance criterion model for story acceptance criteria."""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class AcceptanceCriterion(Base):
    """Acceptance criterion row for a story.
    
    Each story may have multiple acceptance criteria.
    Display order must be unique within a story.
    """
    __tablename__ = "acceptance_criteria"
    
    # Primary key as Integer
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Foreign key to stories.id with cascade delete
    story_id = Column(
        Integer, 
        ForeignKey("stories.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Criterion text content
    criterion_text = Column(String(500), nullable=False)  # max 500 chars per LLD
    
    # Display ordering within the story
    display_order = Column(Integer, nullable=False)  # Positive integer, unique within story
    
    # Standard audit timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    story = relationship("Story", back_populates="acceptance_criteria")
    
    # Unique constraint: one display_order per story
    __table_args__ = (
        UniqueConstraint("story_id", "display_order", name="uq_criteria_order"),
    )
    
    def __repr__(self):
        return f"<AcceptanceCriterion(id={self.id}, story_id={self.story_id}, display_order={self.display_order})>"

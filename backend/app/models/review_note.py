"""Review note model for lightweight reviewer comments."""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class ReviewNote(Base):
    """Lightweight reviewer comment on a workspace.
    
    Flat note model without threading, statuses, or mentions.
    Notes are appended chronologically.
    """
    __tablename__ = "review_notes"
    
    # Primary key as Integer
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Foreign key to workspaces.id with cascade delete
    workspace_id = Column(
        Integer, 
        ForeignKey("workspaces.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Reviewer identification
    reviewer_name = Column(String(80), nullable=False)  # 2-80 chars per LLD
    
    # Note content
    note_text = Column(Text, nullable=False)  # 1-1000 chars validated in schema
    
    # Timestamp
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="review_notes")
    
    def __repr__(self):
        return f"<ReviewNote(id={self.id}, workspace_id={self.workspace_id}, reviewer_name='{self.reviewer_name}')>"

"""Workspace model for single product-definition workspace per user."""
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


class Workspace(Base):
    """Single product-definition workspace per learner.
    
    Contains product metadata, vision fields, business context.
    Enforces one workspace per owner_user_id via unique constraint.
    """
    __tablename__ = "workspaces"
    
    # Primary key as Integer
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Foreign key to users.id with cascade delete
    owner_user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Product identity fields
    product_name = Column(String(120), nullable=False)
    short_description = Column(String(280), nullable=True)
    
    # Vision section fields
    vision_statement = Column(Text, nullable=True)  # max 1000 chars validated in schema
    target_problem = Column(Text, nullable=True)    # max 1000 chars validated in schema
    
    # Business goals and success measures stored as JSON arrays
    # Using Text to store JSON strings for SQLite/PostgreSQL portability
    business_goals_json = Column(Text, nullable=False, default="[]")
    success_measures_json = Column(Text, nullable=False, default="[]")
    
    # Workspace status tracking
    status = Column(String(50), nullable=False, default="EMPTY")
    # Valid statuses: EMPTY, DRAFTING_VISION, DRAFTING_BACKLOG, NEEDS_ATTENTION, 
    #                 READY_FOR_REVIEW, UNDER_REVIEW, REFINEMENT
    
    # Standard audit timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    stories = relationship(
        "Story", 
        back_populates="workspace", 
        cascade="all, delete-orphan",
        order_by="Story.backlog_order"
    )
    
    review_share = relationship(
        "ReviewShare", 
        back_populates="workspace", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    
    review_notes = relationship(
        "ReviewNote", 
        back_populates="workspace", 
        cascade="all, delete-orphan",
        order_by="ReviewNote.created_at"
    )
    
    # Unique constraint: one workspace per user
    __table_args__ = (
        UniqueConstraint("owner_user_id", name="uq_workspace_owner"),
    )
    
    def __repr__(self):
        return f"<Workspace(id={self.id}, product_name='{self.product_name}', owner_user_id={self.owner_user_id})>"

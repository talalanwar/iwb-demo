"""Review share model for protected reviewer access."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class ReviewShare(Base):
    """Protected review access token and metadata.
    
    One share token per workspace for reviewer access.
    Token must be unique across all workspaces.
    """
    __tablename__ = "review_shares"
    
    # Primary key as Integer
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Foreign key to workspaces.id with cascade delete (one-to-one)
    workspace_id = Column(
        Integer, 
        ForeignKey("workspaces.id", ondelete="CASCADE"), 
        nullable=False,
        unique=True,  # One share per workspace
        index=True
    )
    
    # Share token for protected access
    share_token = Column(String(64), nullable=False, unique=True, index=True)
    
    # Access control flag
    requires_auth = Column(Boolean, nullable=False, default=True)
    
    # Creator tracking
    created_by_user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # Optional expiry
    
    # Relationships
    workspace = relationship("Workspace", back_populates="review_share")
    
    def __repr__(self):
        return f"<ReviewShare(id={self.id}, workspace_id={self.workspace_id}, share_token='{self.share_token[:8]}...')>"

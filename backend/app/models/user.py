"""User model for learner identity and authentication."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class User(Base):
    """Learner identity and minimal auth profile.
    
    Stores email, password hash, and display name.
    One user owns one workspace in MVP scope.
    """
    __tablename__ = "users"
    
    # Primary key as Integer auto-increment per task requirements
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    
    # Email uniqueness enforced
    email = Column(String(255), nullable=False, unique=True, index=True)
    
    # Password stored as adaptive hash (bcrypt)
    password_hash = Column(String(255), nullable=False)
    
    # Display name for UI presentation
    display_name = Column(String(255), nullable=False)
    
    # Standard audit timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete support
    deleted_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', display_name='{self.display_name}')>"

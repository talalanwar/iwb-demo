"""Repository for User model persistence operations."""
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Repository for User model data access."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
    
    def get_by_email(self, email: str) -> User | None:
        """Fetch user by email address.
        
        Args:
            email: User email address
            
        Returns:
            User instance if found, None otherwise
        """
        return self.db.query(User).filter(
            User.email == email,
            User.deleted_at.is_(None)
        ).first()
    
    def get_by_id(self, user_id: int) -> User | None:
        """Fetch user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User instance if found and not deleted, None otherwise
        """
        return self.db.query(User).filter(
            User.id == user_id,
            User.deleted_at.is_(None)
        ).first()
    
    def create(self, email: str, password_hash: str, display_name: str) -> User:
        """Create a new user.
        
        Args:
            email: User email address
            password_hash: Hashed password
            display_name: User display name
            
        Returns:
            Created User instance
        """
        user = User(
            email=email,
            password_hash=password_hash,
            display_name=display_name
        )
        self.db.add(user)
        self.db.flush()
        return user

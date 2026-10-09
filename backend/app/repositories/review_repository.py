"""Repository for ReviewShare and ReviewNote model persistence operations."""
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.review_note import ReviewNote
from app.models.review_share import ReviewShare


class ReviewRepository:
    """Repository for ReviewShare and ReviewNote model data access."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session.
        
        Args:
            db: SQLAlchemy session for database operations
        """
        self.db = db
    
    def get_share_by_token(self, share_token: str) -> ReviewShare | None:
        """Fetch review share by token.
        
        Args:
            share_token: Share token string
            
        Returns:
            ReviewShare instance if found and not expired, None otherwise
        """
        share = self.db.query(ReviewShare).filter(
            ReviewShare.share_token == share_token
        ).first()
        
        if not share:
            return None
        
        # Check expiry if set
        if share.expires_at and share.expires_at < datetime.now(UTC):
            return None
        
        return share
    
    def get_share_by_workspace(self, workspace_id: int) -> ReviewShare | None:
        """Fetch review share by workspace ID.
        
        Args:
            workspace_id: Workspace ID
            
        Returns:
            ReviewShare instance if found, None otherwise
        """
        return self.db.query(ReviewShare).filter(
            ReviewShare.workspace_id == workspace_id
        ).first()
    
    def create_share(
        self,
        workspace_id: int,
        share_token: str,
        created_by_user_id: int,
        requires_auth: bool = True,
        expires_at: datetime | None = None
    ) -> ReviewShare:
        """Create a new review share.
        
        Args:
            workspace_id: Workspace ID
            share_token: Unique share token
            created_by_user_id: User ID who created the share
            requires_auth: Whether auth is required (default True)
            expires_at: Optional expiration timestamp
            
        Returns:
            Created ReviewShare instance
        """
        share = ReviewShare(
            workspace_id=workspace_id,
            share_token=share_token,
            created_by_user_id=created_by_user_id,
            requires_auth=requires_auth,
            expires_at=expires_at
        )
        self.db.add(share)
        self.db.flush()
        return share
    
    def get_notes_for_workspace(self, workspace_id: int) -> list[ReviewNote]:
        """Fetch all review notes for a workspace ordered by created_at.
        
        Args:
            workspace_id: Workspace ID
            
        Returns:
            List of ReviewNote instances
        """
        return self.db.query(ReviewNote).filter(
            ReviewNote.workspace_id == workspace_id
        ).order_by(ReviewNote.created_at).all()
    
    def create_note(
        self,
        workspace_id: int,
        reviewer_name: str,
        note_text: str
    ) -> ReviewNote:
        """Create a new review note.
        
        Args:
            workspace_id: Workspace ID
            reviewer_name: Reviewer name
            note_text: Note text content
            
        Returns:
            Created ReviewNote instance
        """
        note = ReviewNote(
            workspace_id=workspace_id,
            reviewer_name=reviewer_name,
            note_text=note_text
        )
        self.db.add(note)
        self.db.flush()
        return note

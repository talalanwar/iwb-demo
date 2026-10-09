"""Database engine and session configuration.

Provides sync SQLAlchemy engine factory reading DATABASE_URL from environment.
Default: sqlite:///./app.db for zero-config local development.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Declarative base for all models
Base = declarative_base()

# Global engine and session factory (initialized on first use)
_engine = None
_SessionLocal = None


def get_database_url() -> str:
    """Return DATABASE_URL from environment or default SQLite."""
    return os.getenv("DATABASE_URL", "sqlite:///./app.db")


def create_db_engine():
    """Create sync SQLAlchemy engine for the configured database."""
    database_url = get_database_url()
    
    # SQLite-specific configuration for better concurrency
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args = {
            "check_same_thread": False  # Allow multiple threads in FastAPI
        }
    
    engine = create_engine(
        database_url,
        connect_args=connect_args,
        echo=False  # Set to True for SQL query debugging
    )
    return engine


def get_engine():
    """Get or create the global engine instance."""
    global _engine
    if _engine is None:
        _engine = create_db_engine()
    return _engine


def get_session_factory():
    """Get or create the global session factory."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine()
        )
    return _SessionLocal


def get_db() -> Session:
    """Dependency to get database session.
    
    Yields a database session that is automatically closed after use.
    Example usage in FastAPI:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables.
    
    This is called from the lifespan context in main.py.
    In production, use Alembic migrations instead.
    """
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

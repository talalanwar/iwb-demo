"""Main FastAPI application with lifespan, CORS, and route registration."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, review, workspace
from app.core.config import settings
from app.core.database import get_engine
from app.core.errors import (
    handle_authorization_error,
    handle_not_found_error,
    handle_server_error,
    handle_unauthorized_error,
    handle_validation_error,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events.
    
    Runs database migration check and seed data on startup.
    """
    logger.info("Starting Product Learning Studio backend...")
    
    # Check database connection
    engine = get_engine()
    try:
        with engine.connect():
            logger.info("Database connection verified")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
    
    # Run migrations (handled by docker-entrypoint.sh or start.sh)
    # Alembic upgrade head should be run before starting the app
    
    # Seed data if needed
    try:
        from app.core.database import get_db
        from app.seed import seed_data
        
        db = next(get_db())
        try:
            seed_data(db)
            logger.info("Seed data initialized")
        finally:
            db.close()
    except Exception:
        logger.warning("Seed data initialization skipped (may already exist)")
    
    logger.info("Backend startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Product Learning Studio backend...")
    get_engine().dispose()


# Create FastAPI app
app = FastAPI(
    title="Product Learning Studio",
    description="Backend API for Product Learning Studio demo SaaS application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(401, handle_unauthorized_error)
app.add_exception_handler(403, handle_authorization_error)
app.add_exception_handler(404, handle_not_found_error)
app.add_exception_handler(422, handle_validation_error)
app.add_exception_handler(500, handle_server_error)

# Register API routes under /api/v1 prefix
API_V1_PREFIX = "/api/v1"

app.include_router(
    auth.router,
    prefix=API_V1_PREFIX,
    tags=["auth"]
)

app.include_router(
    workspace.router,
    prefix=API_V1_PREFIX,
    tags=["workspace"]
)

app.include_router(
    review.router,
    prefix=API_V1_PREFIX,
    tags=["review"]
)


@app.get("/")
def root():
    """Root endpoint for health check."""
    return {
        "message": "Product Learning Studio API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}

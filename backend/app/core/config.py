"""
Core configuration using Pydantic Settings.
Loads settings from environment variables with defaults for local development.
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All configuration should be loaded through environment variables
    to support portability across local, Docker, and production environments.
    """
    # Database configuration
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # JWT authentication configuration
    JWT_SECRET_KEY: str = "dev-secret-key-change-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Application metadata
    APP_NAME: str = "Product Learning Studio"
    APP_VERSION: str = "0.1.0"
    
    # CORS configuration - can be string (comma-separated) or list
    CORS_ORIGINS: str | list[str] = "http://localhost:5173,http://localhost:3000"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Singleton settings instance
settings = Settings()

"""
Application configuration settings
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://prepp.ai",
        "https://www.prepp.ai",
    ]

    # Database
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    DATABASE_URL: str = ""

    # AI Providers
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # External APIs
    SNL_API_KEY: str = ""
    SNL_BASE_URL: str = "https://snl.no/api/v1"

    # App Settings
    MAX_BRIEF_TOKENS: int = 4000
    MAX_RAG_CHUNKS: int = 8
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "claude-3-5-sonnet-20241022"

    # Development
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }


# Create global settings instance
settings = Settings()

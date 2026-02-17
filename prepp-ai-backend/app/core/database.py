"""
Database connection and session management
"""

from typing import AsyncGenerator
import asyncpg
from supabase import create_client, Client

from app.core.config import settings

# Global Supabase client
supabase: Client = create_client(
    supabase_url=settings.SUPABASE_URL,
    supabase_key=settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY,
)

# Global connection pool
_pool: asyncpg.Pool | None = None


async def init_db_pool() -> asyncpg.Pool:
    """Initialize the database connection pool. Call once at startup."""
    global _pool
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL not configured")
    _pool = await asyncpg.create_pool(
        settings.DATABASE_URL,
        min_size=2,
        max_size=10,
    )
    return _pool


async def close_db_pool() -> None:
    """Close the connection pool. Call once at shutdown."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """FastAPI dependency that acquires a connection from the pool."""
    if _pool is None:
        raise RuntimeError("Database pool not initialized. Call init_db_pool() first.")
    async with _pool.acquire() as conn:
        yield conn


def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return supabase

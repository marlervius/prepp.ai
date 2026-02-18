"""
Database connection and session management
"""

from typing import AsyncGenerator, Optional
import asyncpg
from supabase import create_client, Client

from app.core.config import settings

# Global Supabase client (lazy init)
_supabase: Optional[Client] = None

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def init_db_pool() -> asyncpg.Pool:
    """Initialize the database connection pool. Called once at startup."""
    global _pool
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL is not set.")
    _pool = await asyncpg.create_pool(
        settings.DATABASE_URL,
        min_size=2,
        max_size=10,
    )
    return _pool


async def close_db_pool() -> None:
    """Close the connection pool. Called once at shutdown."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """FastAPI dependency — acquires a connection from the pool."""
    if _pool is None:
        raise RuntimeError("Database pool not initialized. Call init_db_pool() first.")
    async with _pool.acquire() as conn:
        yield conn


async def create_db_connection() -> asyncpg.Connection:
    """
    Create a one-off asyncpg connection (for scripts/seeds).
    Remember to call conn.close() when done.
    """
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL is not set.")
    return await asyncpg.connect(settings.DATABASE_URL)


def get_supabase_client() -> Client:
    """Get (or lazily create) the Supabase client instance."""
    global _supabase
    if _supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set.")
        key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
        _supabase = create_client(
            supabase_url=settings.SUPABASE_URL,
            supabase_key=key,
        )
    return _supabase

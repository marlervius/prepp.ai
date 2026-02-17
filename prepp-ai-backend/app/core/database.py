"""
Database connection and session management
"""

from typing import AsyncGenerator, Optional
import asyncpg
from supabase import create_client, Client

from app.core.config import settings

# Global Supabase client
_supabase: Optional[Client] = None


def get_supabase_client() -> Client:
    """Get (or lazily create) the Supabase client instance"""
    global _supabase
    if _supabase is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set to use the Supabase client"
            )
        key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
        _supabase = create_client(
            supabase_url=settings.SUPABASE_URL,
            supabase_key=key,
        )
    return _supabase


async def create_db_connection() -> asyncpg.Connection:
    """
    Create and return a raw asyncpg connection.

    Used by:
    - scripts/seed_lk20_data.py
    - One-off utility scripts

    Remember to call conn.close() when done.
    """
    if not settings.DATABASE_URL:
        raise ValueError(
            "DATABASE_URL is not set. Add it to your .env file."
        )
    return await asyncpg.connect(settings.DATABASE_URL)


async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    FastAPI dependency that yields an asyncpg connection
    and closes it when the request is done.

    Usage:
        @router.get("/...")
        async def handler(conn: asyncpg.Connection = Depends(get_db_connection)):
            ...
    """
    conn = await create_db_connection()
    try:
        yield conn
    finally:
        await conn.close()

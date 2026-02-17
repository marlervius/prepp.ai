"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import asyncpg
from app.core.database import get_db_connection

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "service": "prepp-ai-backend"}

@router.get("/health/db")
async def database_health_check(conn: asyncpg.Connection = Depends(get_db_connection)):
    """Database health check"""
    try:
        result = await conn.fetchval("SELECT 1")
        return {"status": "healthy", "database": "connected", "result": result}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)},
        )

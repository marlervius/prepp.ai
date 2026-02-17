"""
Prepp.ai - FastAPI Backend
Main application entry point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
import time

from app.api.routes import briefs, health
from app.core.config import settings
from app.core.database import init_db_pool, close_db_pool
from app.core.logging import setup_logging
from app.services.cache_service import CacheService

# Setup structured logging
setup_logging()

logger = structlog.get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    logger.info("Starting Prepp.ai backend")

    # Startup
    try:
        pool = await init_db_pool()
        async with pool.acquire() as conn:
            await conn.execute("SELECT 1")
        logger.info("Database connection pool established")
    except Exception as e:
        logger.error("Failed to connect to database", error=str(e))
        raise

    yield

    # Shutdown
    await CacheService.close()
    await close_db_pool()
    logger.info("Shutting down Prepp.ai backend")

# Create FastAPI app
app = FastAPI(
    title="Prepp.ai API",
    description="AI-powered teaching brief generator for Norwegian educators",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log request
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host,
    )

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log response
        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            process_time_ms=round(process_time * 1000, 2),
        )

        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            "Request failed",
            method=request.method,
            url=str(request.url),
            error=str(e),
            process_time_ms=round(process_time * 1000, 2),
        )
        raise

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception",
        error=str(exc),
        url=str(request.url),
        method=request.method,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(briefs.router, prefix="/api/v1", tags=["briefs"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Prepp.ai API", "version": "1.0.0", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,  # Use our custom logging
    )
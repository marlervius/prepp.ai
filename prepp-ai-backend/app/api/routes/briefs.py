"""
Briefs API routes - Main functionality for generating teaching briefs
"""

import json
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, field_validator
import asyncpg
import structlog

from app.core.database import get_db_connection, get_supabase_client
from app.services.ai_pipeline import AIPipeline
from app.services.rag_service import RAGService
from app.services.cache_service import CacheService

logger = structlog.get_logger(__name__)

router = APIRouter()

VALID_SUBJECTS = [
    "Norsk", "Matematikk", "Engelsk", "Naturfag", "Samfunnsfag",
    "Historie", "Geografi", "Religion og etikk", "Kunst og håndverk",
    "Musikk", "Kroppsøving", "Fysikk", "Kjemi", "Biologi",
]

VALID_GRADES = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "VG1", "VG2", "VG3",
]


class BriefRequest(BaseModel):
    """Request model for generating a brief"""
    subject: str = Field(..., description="Fag (fra LK20)")
    grade: str = Field(..., description="Trinn (1-10 eller VG1-VG3)")
    topic: str = Field(..., max_length=200, description="Emne/fritekst")

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, v: str) -> str:
        if v not in VALID_SUBJECTS:
            raise ValueError(f"Ugyldig fag. Gyldige fag: {', '.join(VALID_SUBJECTS)}")
        return v

    @field_validator("grade")
    @classmethod
    def validate_grade(cls, v: str) -> str:
        if v not in VALID_GRADES:
            raise ValueError(f"Ugyldig trinn. Gyldige trinn: {', '.join(VALID_GRADES)}")
        return v


class BriefResponse(BaseModel):
    """Response model for generated brief"""
    id: str
    subject: str
    grade: str
    topic: str
    content: Dict[str, Any]
    sources: List[Dict[str, Any]]
    processing_time_ms: int
    created_at: str


@router.post("/briefs", response_model=BriefResponse)
async def generate_brief(
    request: BriefRequest,
    background_tasks: BackgroundTasks,
    conn: asyncpg.Connection = Depends(get_db_connection),
) -> BriefResponse:
    """
    Generate a teaching brief using AI pipeline and RAG

    This endpoint:
    1. Validates input against LK20 taxonomy
    2. Performs RAG search for relevant sources
    3. Generates structured brief using AI
    4. Caches result for future requests
    5. Logs usage for analytics
    """
    start_time = time.time()

    try:
        logger.info(
            "Brief generation started",
            subject=request.subject,
            grade=request.grade,
            topic=request.topic,
        )

        # Initialize services
        rag_service = RAGService(conn)
        ai_pipeline = AIPipeline()
        cache_service = CacheService()

        # Check cache first
        cache_key = f"brief:{request.subject}:{request.grade}:{request.topic}"
        cached_result = await cache_service.get(cache_key)
        if cached_result:
            logger.info("Returning cached brief", cache_key=cache_key)
            return BriefResponse(**cached_result)

        # Perform RAG search
        rag_context = await rag_service.search_context(
            subject=request.subject,
            grade=request.grade,
            topic=request.topic,
        )

        # Generate brief using AI pipeline
        brief_content = await ai_pipeline.generate_brief(
            subject=request.subject,
            grade=request.grade,
            topic=request.topic,
            rag_context=rag_context,
        )

        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)

        # Create brief record
        brief_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        sources = rag_context.get("sources", [])

        brief_data = {
            "id": brief_id,
            "subject": request.subject,
            "grade": request.grade,
            "topic": request.topic,
            "content": brief_content,
            "sources": sources,
            "processing_time_ms": processing_time,
            "created_at": created_at,
        }

        # Save to database (user_id is NULL for anonymous users, JSON-serialize dicts)
        await conn.execute("""
            INSERT INTO briefs (id, user_id, subject, grade, topic, content, sources, processing_time_ms)
            VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7::jsonb, $8)
        """, brief_id, None, request.subject, request.grade, request.topic,
             json.dumps(brief_content), json.dumps(sources), processing_time)

        # Cache result
        await cache_service.set(cache_key, brief_data, ttl=3600)

        # Log usage in background
        background_tasks.add_task(log_usage, brief_id, processing_time)

        logger.info(
            "Brief generation completed",
            brief_id=brief_id,
            processing_time_ms=processing_time,
        )

        return BriefResponse(**brief_data)

    except HTTPException:
        raise
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        logger.error(
            "Brief generation failed",
            error=str(e),
            processing_time_ms=processing_time,
        )
        raise HTTPException(status_code=500, detail="Failed to generate brief")


async def log_usage(brief_id: str, processing_time_ms: int):
    """Log usage for analytics"""
    try:
        supabase = get_supabase_client()
        logger.info("Usage logged", brief_id=brief_id, processing_time_ms=processing_time_ms)
    except Exception as e:
        logger.error("Failed to log usage", error=str(e))


@router.get("/briefs/{brief_id}")
async def get_brief(
    brief_id: str,
    conn: asyncpg.Connection = Depends(get_db_connection),
) -> BriefResponse:
    """Get a specific brief by ID"""
    try:
        row = await conn.fetchrow("""
            SELECT id, subject, grade, topic, content, sources, processing_time_ms, created_at
            FROM briefs
            WHERE id = $1
        """, brief_id)

        if not row:
            raise HTTPException(status_code=404, detail="Brief not found")

        return BriefResponse(
            id=str(row["id"]),
            subject=row["subject"],
            grade=row["grade"],
            topic=row["topic"],
            content=row["content"] if isinstance(row["content"], dict) else json.loads(row["content"]),
            sources=row["sources"] if isinstance(row["sources"], list) else json.loads(row["sources"] or "[]"),
            processing_time_ms=row["processing_time_ms"],
            created_at=row["created_at"].isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get brief", brief_id=brief_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve brief")

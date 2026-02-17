"""
RAG (Retrieval-Augmented Generation) Service
Handles semantic search and context retrieval from vector database
"""

import json
from typing import Dict, Any, List
import asyncpg
import structlog
from openai import AsyncOpenAI

from app.core.config import settings

logger = structlog.get_logger(__name__)


def _vec_to_str(embedding: List[float]) -> str:
    """Convert embedding list to pgvector string format: '[0.1,0.2,...]'"""
    return "[" + ",".join(str(x) for x in embedding) + "]"


class RAGService:
    """Service for retrieving relevant context using vector similarity search"""

    _openai: AsyncOpenAI | None = None

    def __init__(self, db_connection: asyncpg.Connection):
        self.db = db_connection
        self.embedding_model = settings.EMBEDDING_MODEL

    @property
    def openai(self) -> AsyncOpenAI:
        if RAGService._openai is None:
            RAGService._openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        return RAGService._openai

    async def search_context(
        self,
        subject: str,
        grade: str,
        topic: str,
        max_chunks: int | None = None,
    ) -> Dict[str, Any]:
        """
        Search for relevant context using RAG

        Args:
            subject: Norwegian subject
            grade: Grade level
            topic: Topic to search for
            max_chunks: Maximum number of chunks to retrieve

        Returns:
            Dictionary with retrieved context
        """

        if max_chunks is None:
            max_chunks = settings.MAX_RAG_CHUNKS

        search_query = ""
        try:
            # Create search query by combining inputs
            search_query = f"{subject} {grade} {topic}"

            # Generate embedding for search query
            embedding = await self._generate_embedding(search_query)

            # Search LK20 goals
            lk20_goals = await self._search_lk20_goals(embedding, subject, grade)

            # Search source chunks
            source_chunks = await self._search_source_chunks(embedding, subject, grade, max_chunks)

            # Extract sources for citation
            sources = []
            for chunk in source_chunks:
                sources.append({
                    "title": chunk.get("title", "Uten tittel"),
                    "url": chunk["url"],
                    "source": chunk["source"]
                })

            logger.info(
                "RAG search completed",
                subject=subject,
                grade=grade,
                topic=topic,
                lk20_results=len(lk20_goals),
                source_results=len(source_chunks),
            )

            return {
                "lk20_goals": lk20_goals,
                "source_chunks": source_chunks,
                "sources": sources,
                "search_query": search_query,
            }

        except Exception as e:
            logger.error("RAG search failed", error=str(e))
            return {
                "lk20_goals": [],
                "source_chunks": [],
                "sources": [],
                "search_query": search_query,
            }

    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        try:
            response = await self.openai.embeddings.create(
                input=text,
                model=self.embedding_model,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("Embedding generation failed", error=str(e))
            raise

    async def _search_lk20_goals(
        self,
        query_embedding: List[float],
        subject: str,
        grade: str,
    ) -> List[str]:
        """Search LK20 competence goals"""
        try:
            vec_str = _vec_to_str(query_embedding)

            # First try exact subject/grade match
            exact_results = await self.db.fetch("""
                SELECT goal_text
                FROM lk20_goals
                WHERE subject = $1 AND grade = $2
                ORDER BY embedding <=> $3::vector
                LIMIT 3
            """, subject, grade, vec_str)

            if exact_results:
                return [row["goal_text"] for row in exact_results]

            # Fallback: semantic search across all goals
            semantic_results = await self.db.fetch("""
                SELECT goal_text, subject, grade
                FROM lk20_goals
                ORDER BY embedding <=> $1::vector
                LIMIT 5
            """, vec_str)

            return [f"{row['subject']} {row['grade']}: {row['goal_text']}" for row in semantic_results]

        except Exception as e:
            logger.error("LK20 goals search failed", error=str(e))
            return []

    async def _search_source_chunks(
        self,
        query_embedding: List[float],
        subject: str,
        grade: str,
        max_chunks: int,
    ) -> List[Dict[str, Any]]:
        """Search source chunks with filtering"""
        try:
            vec_str = _vec_to_str(query_embedding)

            # Build metadata filter for subject/grade
            metadata_filter = {}
            if subject:
                metadata_filter["subject"] = subject
            if grade:
                metadata_filter["grade"] = grade

            metadata_json = json.dumps(metadata_filter) if metadata_filter else None

            # Search with metadata filtering
            query = """
                SELECT id, source, url, title, content, metadata, chunk_index
                FROM source_chunks
                WHERE ($3::jsonb IS NULL OR metadata @> $3::jsonb)
                ORDER BY embedding <=> $1::vector
                LIMIT $2
            """

            results = await self.db.fetch(
                query,
                vec_str,
                max_chunks,
                metadata_json,
            )

            # Convert to dict format
            chunks = []
            for row in results:
                chunks.append({
                    "id": str(row["id"]),
                    "source": row["source"],
                    "url": row["url"],
                    "title": row["title"],
                    "content": row["content"],
                    "metadata": dict(row["metadata"]) if row["metadata"] else {},
                    "chunk_index": row["chunk_index"],
                })

            return chunks

        except Exception as e:
            logger.error("Source chunks search failed", error=str(e))
            return []

    async def add_source_chunk(
        self,
        source: str,
        url: str,
        title: str,
        content: str,
        metadata: Dict[str, Any] | None = None,
    ) -> str:
        """Add a new source chunk to the vector database"""
        try:
            # Generate embedding
            embedding = await self._generate_embedding(content)
            vec_str = _vec_to_str(embedding)
            metadata_json = json.dumps(metadata or {})

            # Insert into database
            chunk_id = await self.db.fetchval("""
                INSERT INTO source_chunks (source, url, title, content, embedding, metadata)
                VALUES ($1, $2, $3, $4, $5::vector, $6::jsonb)
                RETURNING id
            """, source, url, title, content, vec_str, metadata_json)

            logger.info("Source chunk added", chunk_id=str(chunk_id), source=source, title=title)
            return str(chunk_id)

        except Exception as e:
            logger.error("Failed to add source chunk", error=str(e))
            raise

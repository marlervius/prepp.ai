"""
Cache Service
Handles Redis caching for briefs and API responses
"""

import json
from typing import Any, Callable, Optional
import redis.asyncio as redis
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)


class CacheService:
    """Redis-based caching service with shared connection"""

    _client: Optional[redis.Redis] = None

    @classmethod
    async def _get_client(cls) -> redis.Redis:
        """Get or create shared Redis client"""
        if cls._client is None:
            cls._client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
            )
        return cls._client

    @classmethod
    async def close(cls) -> None:
        """Close the shared Redis connection. Call at shutdown."""
        if cls._client is not None:
            await cls._client.close()
            cls._client = None

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            client = await self._get_client()
            value = await client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning("Cache get failed", key=key, error=str(e))
            return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL. Value must be JSON-serializable."""
        try:
            client = await self._get_client()
            serialized = json.dumps(value)
            await client.setex(key, ttl, serialized)
            return True
        except (TypeError, ValueError) as e:
            logger.warning("Cache set failed: value not JSON-serializable", key=key, error=str(e))
            return False
        except Exception as e:
            logger.warning("Cache set failed", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            client = await self._get_client()
            await client.delete(key)
            return True
        except Exception as e:
            logger.warning("Cache delete failed", key=key, error=str(e))
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            client = await self._get_client()
            return await client.exists(key) > 0
        except Exception as e:
            logger.warning("Cache exists check failed", key=key, error=str(e))
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        try:
            client = await self._get_client()
            keys = await client.keys(pattern)
            if keys:
                await client.delete(*keys)
            return len(keys)
        except Exception as e:
            logger.warning("Cache clear pattern failed", pattern=pattern, error=str(e))
            return 0

    async def get_or_set(
        self,
        key: str,
        getter_func: Callable,
        ttl: int = 3600,
        force_refresh: bool = False,
    ) -> Any:
        """Get from cache or set using getter function"""
        if not force_refresh:
            cached = await self.get(key)
            if cached is not None:
                logger.debug("Cache hit", key=key)
                return cached

        # Cache miss or force refresh
        logger.debug("Cache miss", key=key)
        value = await getter_func()
        await self.set(key, value, ttl)
        return value

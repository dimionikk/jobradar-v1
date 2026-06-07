from redis.asyncio import Redis
from app.core.config import settings


async def get_redis() -> Redis:
    redis = Redis.from_url(settings.REDIS_URL)
    try:
        yield redis
    finally:
        await redis.aclose()
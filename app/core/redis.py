from redis.asyncio import Redis, ConnectionPool
from app.core.config import settings

pool = ConnectionPool.from_url(settings.REDIS_URL)

async def get_redis() -> Redis:
    async with Redis(connection_pool=pool) as redis:
        yield redis
from redis.asyncio import Redis

from src.core.config import settings


redis_client = Redis.from_url(
    settings.redis_dsn,
    decode_responses=True,
)


async def get_redis() -> Redis:
    return redis_client
from redis.asyncio import Redis


class BlacklistRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def _blacklist_key(jti: str) -> str:
        return f"blacklist:{jti}"

    async def add(self, jti: str, ttl_seconds: int) -> None:
        await self.redis.set(
            self._blacklist_key(jti),
            "1",
            ex=max(ttl_seconds, 1),
        )

    async def exists(self, jti: str) -> bool:
        result = await self.redis.exists(self._blacklist_key(jti))
        return bool(result)
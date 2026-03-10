import json
from datetime import datetime, timedelta, timezone
from uuid import UUID

from redis.asyncio import Redis

from src.core.config import settings


class RefreshRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def _refresh_key(jti: str) -> str:
        return f"refresh:{jti}"

    @staticmethod
    def _user_refresh_key(user_id: UUID | str) -> str:
        return f"user_refresh:{user_id}"

    async def save_refresh_session(
        self,
        jti: str,
        user_id: UUID | str,
        username: str,
    ) -> None:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        payload = {
            "user_id": str(user_id),
            "username": username,
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
        }

        refresh_key = self._refresh_key(jti)
        user_refresh_key = self._user_refresh_key(user_id)

        await self.redis.set(
            refresh_key,
            json.dumps(payload),
            ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
        await self.redis.sadd(user_refresh_key, jti)

    async def get_refresh_session(self, jti: str) -> dict | None:
        data = await self.redis.get(self._refresh_key(jti))
        if not data:
            return None
        return json.loads(data)

    async def delete_refresh_session(
        self,
        jti: str,
        user_id: UUID | str,
    ) -> None:
        refresh_key = self._refresh_key(jti)
        user_refresh_key = self._user_refresh_key(user_id)

        await self.redis.delete(refresh_key)
        await self.redis.srem(user_refresh_key, jti)

    async def delete_all_user_sessions(self, user_id: UUID | str) -> None:
        user_refresh_key = self._user_refresh_key(user_id)
        jtis = await self.redis.smembers(user_refresh_key)

        if jtis:
            keys = [self._refresh_key(jti) for jti in jtis]
            await self.redis.delete(*keys)

        await self.redis.delete(user_refresh_key)
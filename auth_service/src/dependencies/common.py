from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.core.database import get_db
from src.core.redis import get_redis
from src.repositories.blacklist_repository import BlacklistRepository
from src.repositories.refresh_repository import RefreshRepository
from src.repositories.user_repository import UserRepository


def get_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(session)


def get_refresh_repository(
    redis: Redis = Depends(get_redis),
) -> RefreshRepository:
    return RefreshRepository(redis)


def get_blacklist_repository(
    redis: Redis = Depends(get_redis),
) -> BlacklistRepository:
    return BlacklistRepository(redis)
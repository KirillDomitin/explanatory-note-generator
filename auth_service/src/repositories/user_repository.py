from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[User]:
        stmt = select(User).order_by(User.created_at.asc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(
        self,
        username: str,
        password_hash: str,
        role: str,
        is_active: bool = True,
    ) -> User:
        user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            is_active=is_active,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, user: User) -> User:
        await self.session.flush()
        return user
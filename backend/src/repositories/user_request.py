import uuid
from collections.abc import Sequence

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import RequestStatus, UserRequest


class UserRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user_request(
        self,
        user_id: uuid.UUID,
        inn: str,
        status: RequestStatus,
        name: str | None = None,
        error_message: str | None = None,
    ) -> UserRequest:
        user_request = UserRequest(
            user_id=user_id,
            inn=inn,
            name=name,
            status=status,
            error_message=error_message,
        )

        self.session.add(user_request)
        await self.session.commit()
        await self.session.refresh(user_request)

        return user_request

    async def get_user_requests_by_user_id(
        self,
        user_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[UserRequest]:
        stmt = (
            select(UserRequest)
            .where(UserRequest.user_id == user_id)
            .order_by(desc(UserRequest.created_at))
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count_user_requests_by_user_id(self, user_id: uuid.UUID) -> int:
        stmt = select(func.count()).select_from(UserRequest).where(
            UserRequest.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
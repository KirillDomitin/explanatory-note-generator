import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from src.func.deps import get_current_user
from src.repositories import UserRequestRepository
from src.schemas import UserRequestListResponse, UserRequestRead

router = APIRouter(prefix="/user-requests", tags=["user-requests"])


@router.get("", response_model=UserRequestListResponse)
async def get_my_user_requests(
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user),
) -> UserRequestListResponse:
    repo = UserRequestRepository(db)

    user_id = uuid.UUID(current_user["user_id"])

    items = await repo.get_user_requests_by_user_id(
        user_id=user_id,
        limit=limit,
        offset=offset,
    )
    total = await repo.count_user_requests_by_user_id(user_id)

    return UserRequestListResponse(
        items=[UserRequestRead.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )

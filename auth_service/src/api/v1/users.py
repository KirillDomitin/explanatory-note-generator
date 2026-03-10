from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.dependencies.auth_guard import require_admin
from src.dependencies.user import get_user_service
from src.models.user import User
from src.schemas.auth import MessageResponse
from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.services.user_service import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserService,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def list_users(
    _current_admin: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    users = await user_service.list_users()
    return [UserResponse.model_validate(user) for user in users]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    _current_admin: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = await user_service.create_user(data)
        await db.commit()
        await db.refresh(user)
    except UserAlreadyExistsError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except Exception:
        await db.rollback()
        raise

    return UserResponse.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _current_admin: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = await user_service.update_user(user_id, data)
        await db.commit()
        await db.refresh(user)
    except UserNotFoundError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UserAlreadyExistsError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except Exception:
        await db.rollback()
        raise

    return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    _current_admin: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service),
) -> MessageResponse:
    try:
        await user_service.delete_user(user_id)
        await db.commit()
    except UserNotFoundError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except Exception:
        await db.rollback()
        raise

    return MessageResponse(message="user deactivated")
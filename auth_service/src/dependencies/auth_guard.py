from fastapi import Cookie, Depends, HTTPException, status

from src.core.config import settings
from src.dependencies.auth import get_auth_service
from src.models.user import User
from src.services.auth_service import AuthService, UnauthorizedError
from src.utils.enums import UserRole


async def get_current_user(
    access_token: str | None = Cookie(default=None, alias=settings.ACCESS_COOKIE_NAME),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing",
        )

    try:
        return await auth_service.get_current_user_by_access_token(access_token)
    except UnauthorizedError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
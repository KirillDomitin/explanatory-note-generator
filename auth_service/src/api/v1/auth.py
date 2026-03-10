from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from src.core.config import settings
from src.core.security import clear_auth_cookies, set_auth_cookies
from src.dependencies.auth import get_auth_service
from src.dependencies.auth_guard import get_current_user
from src.models.user import User
from src.schemas.auth import LoginRequest, MeResponse, MessageResponse
from src.services.auth_service import (
    AuthService,
    InactiveUserError,
    InvalidCredentialsError,
    UnauthorizedError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/login",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    try:
        access_token, refresh_token, _user = await auth_service.login(
            username=data.username,
            password=data.password,
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
    except InactiveUserError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    set_auth_cookies(
        response=response,
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return MessageResponse(message="login successful")


@router.get("/me", response_model=MeResponse)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post(
    "/refresh",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(
        default=None,
        alias=settings.REFRESH_COOKIE_NAME,
    ),
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing",
        )

    try:
        new_access_token, new_refresh_token = await auth_service.refresh_tokens(
            refresh_token
        )
    except UnauthorizedError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    set_auth_cookies(
        response=response,
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )
    return MessageResponse(message="tokens refreshed")


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def logout(
    response: Response,
    access_token: str | None = Cookie(
        default=None,
        alias=settings.ACCESS_COOKIE_NAME,
    ),
    refresh_token: str | None = Cookie(
        default=None,
        alias=settings.REFRESH_COOKIE_NAME,
    ),
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    await auth_service.logout(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    clear_auth_cookies(response)
    return MessageResponse(message="logout successful")


@router.post(
    "/logout-all",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def logout_all(
    response: Response,
    current_user: User = Depends(get_current_user),
    access_token: str | None = Cookie(
        default=None,
        alias=settings.ACCESS_COOKIE_NAME,
    ),
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    await auth_service.logout_all(
        user=current_user,
        access_token=access_token,
    )
    clear_auth_cookies(response)
    return MessageResponse(message="all sessions revoked")
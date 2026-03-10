import uuid
from datetime import datetime, timezone
from datetime import timedelta
from typing import Any

import jwt
from fastapi import Response
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from src.core.config import settings

password_hasher = PasswordHash.recommended()


class TokenError(Exception):
    pass


class TokenExpiredError(TokenError):
    pass


class InvalidTokenTypeError(TokenError):
    pass


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def _build_token(
        user_id: str,
        token_type: str,
        expires_delta: timedelta,
        secret: str,
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "type": token_type,
        "jti": str(uuid.uuid4()),
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(user_id: str) -> str:
    return _build_token(
        user_id=user_id,
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret=settings.JWT_ACCESS_SECRET,
    )


def create_refresh_token(user_id: str) -> str:
    return _build_token(
        user_id=user_id,
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        secret=settings.JWT_REFRESH_SECRET,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_ACCESS_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except ExpiredSignatureError as exc:
        raise TokenExpiredError("Access token expired") from exc
    except InvalidTokenError as exc:
        raise TokenError("Invalid access token") from exc

    if payload.get("type") != "access":
        raise InvalidTokenTypeError("Token is not an access token")

    return payload


def decode_refresh_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_REFRESH_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except ExpiredSignatureError as exc:
        raise TokenExpiredError("Refresh token expired") from exc
    except InvalidTokenError as exc:
        raise TokenError("Invalid refresh token") from exc

    if payload.get("type") != "refresh":
        raise InvalidTokenTypeError("Token is not a refresh token")

    return payload


def set_auth_cookies(
        response: Response,
        access_token: str,
        refresh_token: str,
) -> None:
    response.set_cookie(
        key=settings.ACCESS_COOKIE_NAME,
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
    )

    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/api/v1/auth",
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        key=settings.ACCESS_COOKIE_NAME,
        path="/",
    )
    response.delete_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        path="/api/v1/auth",
    )


def get_token_ttl_seconds(payload: dict[str, Any]) -> int:
    exp = payload.get("exp")
    if exp is None:
        return 0

    now_ts = int(datetime.now(timezone.utc).timestamp())
    return max(int(exp) - now_ts, 0)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Any
from uuid import UUID

import jwt
from fastapi import Cookie, HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError
from redis.asyncio import Redis

from src.core.config import get_settings

settings = get_settings()

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)


async def get_redis() -> Redis:
    return redis_client


async def get_current_user(
        access_token: str | None = Cookie(default=None, alias=settings.access_cookie_name),
) -> dict[str, Any]:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing",
        )
    try:
        payload = jwt.decode(
            access_token,
            settings.jwt_access_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    jti = payload.get("jti")
    sub = payload.get("sub")

    if not jti or not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    is_blacklisted = await redis_client.exists(f"blacklist:{jti}")
    if is_blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is blacklisted",
        )

    try:
        user_id = UUID(sub)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user id in token",
        )

    return {
        "user_id": str(user_id),
        "jti": jti,
        "payload": payload,
    }

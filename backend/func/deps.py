#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Any
from uuid import UUID

import jwt
import settings
from fastapi import Cookie, HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError
from redis.asyncio import Redis

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


async def get_current_user(
    access_token: str | None = Cookie(default=None, alias=settings.ACCESS_COOKIE_NAME),
) -> dict[str, Any]:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing",
        )
    print(access_token)
    print(access_token)
    print(access_token)
    print(access_token)
    print(access_token)
    print(access_token)
    print(access_token)
    print(access_token)
    print(access_token)
    print(settings.JWT_ACCESS_SECRET)
    print(settings.JWT_ACCESS_SECRET)
    print(settings.JWT_ACCESS_SECRET)
    print(settings.JWT_ACCESS_SECRET)
    print(settings.JWT_ACCESS_SECRET)
    print(settings.JWT_ALGORITHM)
    print(settings.JWT_ALGORITHM)
    print(settings.JWT_ALGORITHM)
    print(settings.JWT_ALGORITHM)
    print(settings.JWT_ALGORITHM)
    try:
        payload = jwt.decode(
            access_token,
            settings.JWT_ACCESS_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
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
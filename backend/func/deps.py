#!/usr/bin/python
# -*- coding: utf-8 -*-
import httpx
from fastapi import Request, HTTPException, status

AUTH_SERVICE_URL = "http://auth_service:8000/api/v1/users/me"


async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_SERVICE_URL,
            headers={"Authorization": auth_header},
            timeout=5,
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return response.json()
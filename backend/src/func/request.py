#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import httpx

from src.core.config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)


async def get_response(url: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url=url, headers=settings.headers)
        return response

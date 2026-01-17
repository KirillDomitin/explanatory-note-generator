#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import httpx

from settings import HEADERS

logger  = logging.getLogger(__name__)


async def get_response(url: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url=url, headers=HEADERS)
        print(response)
        return response
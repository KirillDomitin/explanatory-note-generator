#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from redis.asyncio import Redis


class RedisService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_cached_result(self, inn):
        return await self.redis.get(inn)

    async def set_cached_data(self, inn: str, payload: dict):
        await self.redis.set(
            inn,
            json.dumps(payload),
            ex=24 * 60 * 60,
        )

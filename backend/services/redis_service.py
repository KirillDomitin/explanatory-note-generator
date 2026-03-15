#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging

from redis.asyncio import Redis

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

class RedisService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_cached_result(self, inn):
        cache = await self.redis.get(inn)
        if cache:
            logger.info(f"Результат по {inn} из кэша")
        return json.loads(cache)

    async def set_cached_data(self, inn: str, payload: dict):
        await self.redis.set(
            inn,
            json.dumps(payload),
            ex=24 * 60 * 60,
        )
        logger.info(f"Результат по {inn} закэширован на 24 часа")
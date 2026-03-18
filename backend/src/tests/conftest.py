#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    url: str
    headers: str
    jwt_access_secret: str
    jwt_algorithm: str
    access_cookie_name: str
    redis_host: str
    redis_port: int
    redis_db: int
    auth_postgres_host: str
    auth_postgres_port: int
    auth_postgres_db: str
    auth_postgres_user: str
    auth_postgres_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    url: str = "https://test.local"
    headers: str = "{}"
    jwt_access_secret: str = "test-secret"
    jwt_algorithm: str = "HS256"
    access_cookie_name: str = "access_token"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    auth_postgres_host: str = "localhost"
    auth_postgres_port: int = 5432
    auth_postgres_db: str = "test_db"
    auth_postgres_user: str = "test_user"
    auth_postgres_password: str = "test_password"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
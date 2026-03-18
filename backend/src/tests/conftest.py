#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import os

os.environ.setdefault("URL", "https://test.local")
os.environ.setdefault("HEADERS", "{}")
os.environ.setdefault("JWT_ACCESS_SECRET", "test-secret")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_COOKIE_NAME", "access_token")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("REDIS_DB", "0")
os.environ.setdefault("AUTH_POSTGRES_HOST", "localhost")
os.environ.setdefault("AUTH_POSTGRES_PORT", "5432")
os.environ.setdefault("AUTH_POSTGRES_DB", "test_db")
os.environ.setdefault("AUTH_POSTGRES_USER", "test_user")
os.environ.setdefault("AUTH_POSTGRES_PASSWORD", "test_password")
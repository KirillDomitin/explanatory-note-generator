#!/usr/bin/python
# -*- coding: utf-8 -*-

from fastapi import APIRouter

from .explanatory.router import router as exp_router

api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}

api_router.include_router(exp_router, prefix="/generate", tags=["explanatory"])
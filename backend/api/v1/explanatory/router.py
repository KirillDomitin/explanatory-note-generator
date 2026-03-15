#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import tempfile

import settings
from docxtpl import DocxTemplate
from fastapi import HTTPException, status, Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from func.deps import get_current_user, get_redis
from services.generate_explanatory_note import explanatory_note
from services.redis_service import RedisService

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

router = APIRouter()


@router.get(
    "/",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    responses=settings.RESPONSES,
    summary="Пояснительная записка в ФНС",
    description="Подставляет в шаблон данные из выписки ЕГРЮЛ"
)
async def generate_document(
        inn: int,
        user=Depends(get_current_user),
        cache=Depends(get_redis)
):
    if inn < 100000000 or inn > 999999999999999:
        raise HTTPException(status_code=400, detail="ИНН должен быть 10 или 12 цифр")

    cache_service = RedisService(cache)
    context = await cache_service.get_cached_result(str(inn))

    try:
        if not context:
            context = await explanatory_note(inn)
            await cache_service.set_cached_data(str(inn), context)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        output_path = tmp.name

    try:
        doc = DocxTemplate(settings.TEMPLATE_PATH)
        doc.render(context)
        doc.save(output_path)

        return FileResponse(
            path=output_path,
            filename=f"Пояснения_{inn}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"X-Content-Type-Options": "nosniff"},
        )

    except Exception as e:
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise HTTPException(status_code=500, detail=f"Ошибка генерации документа: {str(e)}")

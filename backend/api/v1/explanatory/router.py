#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import tempfile

from docxtpl import DocxTemplate
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter

import settings
from servises.generate_explanatory_note import explanatory_note

router = APIRouter()


@router.get(
    "/",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    responses=settings.RESPONSES,
    summary="Пояснительная записка в ФНС",
    description="Подставляет в шаблон данные из выписки ЕГРЮЛ"
)
async def generate_document(inn: int):
    """
    Пример вызова:
    http://192.168.1.100:8000/generate/?inn=770101001
    """
    if inn < 100000000 or inn > 999999999999999:
        raise HTTPException(status_code=400, detail="ИНН должен быть 10 или 12 цифр")

    try:
        context = await explanatory_note(inn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")

    # Временный файл для результата
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
            headers={"X-Content-Type-Options": "nosniff"}
        )

    except Exception as e:
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise HTTPException(status_code=500, detail=f"Ошибка генерации документа: {str(e)}")

    finally:
        pass

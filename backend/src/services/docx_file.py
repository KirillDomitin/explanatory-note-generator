#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import tempfile

from docxtpl import DocxTemplate
from fastapi import HTTPException

from src.core.config import get_settings

settings = get_settings()


def create_docx_file(context: dict) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        output_path = tmp.name

    try:
        doc = DocxTemplate(settings.template_path)
        doc.render(context)
        doc.save(output_path)
        return output_path
    except Exception as exc:
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise HTTPException(status_code=500, detail=f"Ошибка генерации документа: {str(exc)}")

import logging
import uuid

from fastapi import HTTPException, status, Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.session import get_db
from src.db.models import RequestStatus
from src.func.deps import get_current_user, get_redis
from src.repositories.user_request import UserRequestRepository
from src.services.docx_file import create_docx_file
from src.services.generate_explanatory_note import explanatory_note
from src.services.redis_service import RedisService

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
    responses=settings.responses,
    summary="Пояснительная записка в ФНС",
    description="Подставляет в шаблон данные из выписки ЕГРЮЛ"
)
async def generate_document(
    inn: int,
    user: dict = Depends(get_current_user),
    cache=Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    if inn < 100000000 or inn > 999999999999999:
        raise HTTPException(status_code=400, detail="ИНН должен быть 10 или 12 цифр")

    user_id = uuid.UUID(user["user_id"])
    repo = UserRequestRepository(db)
    cache_service = RedisService(cache)

    try:
        context = await cache_service.get_cached_result(str(inn))

        if not context:
            context = await explanatory_note(inn)
            await cache_service.set_cached_data(str(inn), context)

        temp_docx_path = create_docx_file(context)

        await repo.create_user_request(
            user_id=user_id,
            inn=str(inn),
            status=RequestStatus.SUCCESS,
            name=context.get("short_company_name"),
            error_message=None,
        )

        return FileResponse(
            path=temp_docx_path,
            filename=f"Пояснения_{inn}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"X-Content-Type-Options": "nosniff"},
        )

    except ValueError as e:
        await repo.create_user_request(
            user_id=user_id,
            inn=str(inn),
            status=RequestStatus.FAILED,
            name=None,
            error_message=str(e),
        )
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        await repo.create_user_request(
            user_id=user_id,
            inn=str(inn),
            status=RequestStatus.FAILED,
            name=None,
            error_message=str(e),
        )
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")
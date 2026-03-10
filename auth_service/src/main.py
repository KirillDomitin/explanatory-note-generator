from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.users import router as users_router
from src.core.config import settings
from src.core.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.ping()
    yield
    await redis_client.aclose()


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/api/openapi",
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)

app.include_router(api_v1_router)
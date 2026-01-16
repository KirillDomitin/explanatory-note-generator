from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import api_router

app = FastAPI(title="Генератор пояснений по ИНН", debug=True)
app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   #["http://localhost:5173"],   # откуда разрешено делать запросы
    allow_credentials=True,
    allow_methods=["*"],                        # GET, POST, PUT и т.д.
    allow_headers=["*"],                        # все заголовки
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # убрать в продакшене
        # log_config=settings.LOGGING_CONFIG,
        # workers=1            # если много запросов — можно увеличить
    )

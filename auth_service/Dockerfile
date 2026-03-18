#FROM python:3.12-slim
#
#WORKDIR /app
#
## системные зависимости
#RUN apt-get update && apt-get install -y \
#    build-essential \
#    && rm -rf /var/lib/apt/lists/*
#
## копируем зависимости
#COPY pyproject.toml ./
#
## ставим uv
#RUN pip install uv
#
## устанавливаем зависимости
#RUN uv pip install --system .
#
## копируем код
#COPY src ./src
#COPY alembic ./alembic
#COPY alembic.ini ./
#
## запуск
##CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
##CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000"]
#CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY . .

RUN uv pip install --system .

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
FROM python:3.12-slim

WORKDIR /app

# системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# копируем зависимости
COPY pyproject.toml ./

# ставим uv
RUN pip install uv

# устанавливаем зависимости
RUN uv pip install --system .

# копируем код
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

# запуск
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
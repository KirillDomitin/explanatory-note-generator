# Стадия 1 — сборка зависимостей
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-install-project

# Финальная стадия
FROM python:3.13-slim

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Копируем код
COPY . .

# Делаем uvicorn исполняемым (на всякий случай)
RUN chmod +x /usr/local/bin/uvicorn

# Запускаем напрямую
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
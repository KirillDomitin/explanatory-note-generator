# Стадия 1 — сборка зависимостей с uv
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Копируем только файлы зависимостей (для кэширования)
COPY pyproject.toml uv.lock* ./

# Создаём venv и устанавливаем всё
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv sync --frozen

# Стадия 2 — финальный образ
FROM python:3.13-slim

WORKDIR /app

# Копируем готовое venv целиком
COPY --from=builder /app/.venv /app/.venv

# Копируем код и шаблон
COPY . .

# venv в PATH (самое важное!)
ENV PATH="/app/.venv/bin:${PATH}"

# Запускаем через python -m uvicorn — работает в 99% случаев
#CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["/app/.venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

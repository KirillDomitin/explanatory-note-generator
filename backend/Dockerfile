# Стадия 1 — сборка зависимостей
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

WORKDIR /app

COPY pyproject.toml uv.lock* ./

# Явно создаём venv с managed python (uv сам скачает и установит python в venv)
RUN uv venv --python-preference managed .venv && \
    . .venv/bin/activate && \
    uv sync --frozen

# Финальная стадия
FROM python:3.13-slim

WORKDIR /app

# Копируем полноценный venv (теперь python внутри будет правильный)
COPY --from=builder /app/.venv /app/.venv

COPY . .

ENV PATH="/app/.venv/bin:${PATH}"

# Запускаем через uvicorn напрямую из venv
CMD ["/app/.venv/bin/uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
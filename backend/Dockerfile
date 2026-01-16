FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /app
COPY pyproject.toml uv.lock* ./

RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv sync --frozen

FROM python:3.13-alpine

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:${PATH}"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

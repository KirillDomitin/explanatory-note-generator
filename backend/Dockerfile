#FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder
#
#WORKDIR /app
#COPY pyproject.toml uv.lock* ./
#
#RUN uv venv --python-preference system .venv && \
#    . .venv/bin/activate && \
#    uv sync --frozen
#
#FROM python:3.13-alpine
#
#WORKDIR /app
#COPY --from=builder /app/.venv /app/.venv
#COPY . .
#
#ENV PATH="/app/.venv/bin:${PATH}"
#
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN pip install uv && uv sync --frozen --system

COPY . .

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN pip install --no-cache-dir uv \
    && uv venv .venv \
    && uv sync --frozen

COPY . .

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

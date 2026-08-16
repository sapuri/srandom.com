FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

ENV UV_COMPILE_BYTECODE=1
RUN uv sync --frozen --no-dev

FROM python:3.11-slim AS runner

WORKDIR /app
COPY --from=builder /app /app
COPY . /app

EXPOSE 8000

ENV PORT=8000

CMD .venv/bin/python manage.py migrate && .venv/bin/python main.py

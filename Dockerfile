# syntax=docker/dockerfile:1.7

FROM node:24-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund

COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS backend-builder
WORKDIR /app/backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy

COPY backend/pyproject.toml backend/uv.lock ./
RUN pip install --upgrade pip && pip install uv
RUN uv sync --frozen --no-dev

COPY backend/app ./app

FROM python:3.12-slim AS runtime
WORKDIR /app

ARG APP_ENV=production
ENV APP_ENV=${APP_ENV} 

RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=backend-builder --chown=app:app /app/backend/.venv /app/backend/.venv
COPY --from=backend-builder --chown=app:app /app/backend/app /app/backend/app
COPY --from=frontend-builder --chown=app:app /app/frontend/dist /app/frontend/dist

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=25s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()" || exit 1

CMD ["/app/backend/.venv/bin/gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]

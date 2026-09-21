# WayFinder Backend

FastAPI + LangGraph backend managed with `uv`.

## Setup

From this `backend/` directory:

```bash
uv sync
```

Create the root environment file if it does not already exist:

```bash
cd ..
cp .env.example .env
```

Set `GOOGLE_API_KEY` in `.env`.

## Run

From the repository root:

```bash
cd backend
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

From this `backend/` directory:

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The public frontend should reach this service through Nginx at `/api/*`, not by calling port `8000` directly.

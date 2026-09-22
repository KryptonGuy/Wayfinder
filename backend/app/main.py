from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.graph.workflow import run_chat, stream_chat
from app.schemas import ChatRequest, ChatResponse

settings = get_settings()

app = FastAPI(title="WayFinder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="frontend-assets")

    @app.get("/{path:path}", include_in_schema=False)
    async def serve_frontend(path: str | None = None):
        if path and path.startswith("api"):
            raise HTTPException(status_code=404, detail="Not found")
        return FileResponse(frontend_dist / "index.html")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        content = await run_chat(request.messages)
        return ChatResponse(message=content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to generate a response") from exc


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    async def token_stream():
        try:
            async for token in stream_chat(request.messages):
                yield token
        except Exception:
            yield "\n[WayFinder error: unable to generate a response]"

    return StreamingResponse(token_stream(), media_type="text/plain")
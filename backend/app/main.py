from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

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
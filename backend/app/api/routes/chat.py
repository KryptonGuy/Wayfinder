from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas import ChatRequest, ChatResponse
from app.services.chat import run_chat, stream_chat

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        content = await run_chat(request.messages)
        return ChatResponse(message=content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to generate a response") from exc


@router.post("/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    async def token_stream():
        try:
            async for token in stream_chat(request.messages):
                yield token
        except Exception:
            yield "\n[WayFinder error: unable to generate a response]"

    return StreamingResponse(token_stream(), media_type="text/plain")

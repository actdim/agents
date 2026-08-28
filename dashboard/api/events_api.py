"""Server-Sent Events (SSE) live updates endpoint."""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from ..core.watcher import RepoWatcher

router = APIRouter(tags=["Events"])


@router.get("/events", summary="Stream live repository changes via Server-Sent Events (SSE)")
async def stream_events(request: Request):
    watcher: RepoWatcher = request.app.state.watcher
    return StreamingResponse(
        watcher.event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


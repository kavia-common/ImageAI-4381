import time
from typing import Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, WebSocket, WebSocketDisconnect
from app.models.schemas import VideoJobResponse, VideoStatusResponse, ErrorResponse
from app.services.video_service import VideoService
from app.core.config import settings
from app.websocket.manager import ws_manager

router = APIRouter()
_service = VideoService(upload_dir=settings.UPLOAD_DIR, output_dir=settings.OUTPUT_DIR, ws_manager=ws_manager)

# PUBLIC_INTERFACE
@router.post(
    "/video/detect",
    response_model=VideoJobResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Start video detection job",
    description="Uploads a video and starts background detection. Returns a job_id.",
)
async def video_detect(
    file: UploadFile = File(..., description="Video file to process"),
    model_name: Optional[str] = Form(None, description="Optional detection model name"),
    confidence: float = Form(0.5, description="Minimum confidence threshold [0-1]"),
):
    start = time.time()
    try:
        job = await _service.start_job(file, confidence=confidence, model_name=model_name)
        job.elapsed = time.time() - start
        return job
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video detection failed: {e}") from e


# PUBLIC_INTERFACE
@router.get(
    "/video/status/{job_id}",
    response_model=VideoStatusResponse,
    responses={404: {"model": ErrorResponse}},
    summary="Get video job status",
    description="Returns current progress and output path if completed.",
)
async def video_status(job_id: str):
    try:
        return await _service.status(job_id)
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=str(ke)) from ke


# PUBLIC_INTERFACE
@router.websocket("/ws/video/{job_id}")
async def video_progress_ws(websocket: WebSocket, job_id: str):
    """WebSocket that streams progress updates for a given video detection job_id."""
    await ws_manager.connect(job_id, websocket)
    try:
        while True:
            # Keep connection alive; server pushes updates; client may ping
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(job_id, websocket)

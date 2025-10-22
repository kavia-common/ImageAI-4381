import time
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.models.schemas import DetectionResponse, ErrorResponse
from app.services.detection_service import DetectionService
from app.core.config import settings

router = APIRouter()

_service = DetectionService(upload_dir=settings.UPLOAD_DIR, output_dir=settings.OUTPUT_DIR)

# PUBLIC_INTERFACE
@router.post(
    "/detect",
    response_model=DetectionResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Detect objects in an image",
    description="Accepts an image and returns detections with bounding boxes. Saves annotated output to static outputs.",
)
async def detect_objects(
    file: UploadFile = File(..., description="Image file to detect objects in"),
    model_name: Optional[str] = Form(None, description="Optional detection model name to use"),
    confidence: float = Form(0.5, description="Minimum confidence threshold [0-1]"),
):
    start = time.time()
    try:
        result = await _service.detect(file, confidence=confidence, model_name=model_name)
        result.elapsed = time.time() - start
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {e}") from e

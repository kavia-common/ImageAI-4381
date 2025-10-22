import time
from typing import Optional

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.models.schemas import ClassificationResponse, ErrorResponse
from app.services.classification_service import ClassificationService
from app.core.config import settings

router = APIRouter()

_service = ClassificationService(upload_dir=settings.UPLOAD_DIR)

# PUBLIC_INTERFACE
@router.post(
    "/classify",
    response_model=ClassificationResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Classify an image",
    description="Accepts an image and returns top-k predictions.",
)
async def classify_image(
    file: UploadFile = File(..., description="Image file to classify"),
    top_k: int = Form(5, description="Number of top predictions to return"),
    model_name: Optional[str] = Form(None, description="Optional model name to use"),
):
    start = time.time()
    try:
        result = await _service.classify(file, top_k=top_k, model_name=model_name)
        result.elapsed = time.time() - start
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {e}") from e

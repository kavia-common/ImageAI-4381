import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.routes_classification import router as classification_router
from app.api.v1.routes_detection import router as detection_router
from app.api.v1.routes_video import router as video_router
from app.core.config import settings, openapi_tags
from app.core.devices import get_device_info

# Ensure data directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

app = FastAPI(
    title="ImageAI Backend API",
    description="FastAPI backend for ImageAI image classification, object detection, and video detection.",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

# CORS configuration: read from env ALLOW_ORIGINS (comma-separated), fallback to localhost:5173
allow_origins_env = os.environ.get("ALLOW_ORIGINS", "http://localhost:5173")
allow_origins = [o.strip() for o in allow_origins_env.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to serve outputs/artifacts
app.mount("/static", StaticFiles(directory=settings.DATA_DIR), name="static")

# Register routers
app.include_router(classification_router, prefix="/api/v1", tags=["classification"])
app.include_router(detection_router, prefix="/api/v1", tags=["detection"])
app.include_router(video_router, prefix="/api/v1", tags=["video", "websocket"])


# PUBLIC_INTERFACE
@app.get("/api/v1/health", tags=["health"], summary="Health check and environment info")
def health():
    """Returns health and environment details including device and version info."""
    start = time.time()
    device_info = get_device_info()
    elapsed = time.time() - start
    return {
        "status": "ok",
        "elapsed": elapsed,
        "device": device_info,
        "versions": {
            "fastapi": "0.115.x",
            "pydantic": "2.x",
            "python": os.environ.get("PYTHON_VERSION", "3.10"),
            "opencv": _try_import_version("cv2"),
            "torch": _try_import_version("torch"),
            "pillow": _try_import_version("PIL"),
            "imageai": _try_import_version("imageai"),
        },
        "static": {
            "uploads": f"/static/uploads",
            "outputs": f"/static/outputs",
        },
    }


def _try_import_version(mod_name: str) -> str:
    try:
        if mod_name == "PIL":
            import PIL
            return getattr(PIL, "__version__", "unknown")
        module = __import__(mod_name)
        return getattr(module, "__version__", "unknown")
    except Exception:
        return "not-installed"

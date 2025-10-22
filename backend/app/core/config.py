import os
from pydantic import BaseModel

class Settings(BaseModel):
    BASE_DIR: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    UPLOAD_DIR: str = os.path.join(DATA_DIR, "uploads")
    OUTPUT_DIR: str = os.path.join(DATA_DIR, "outputs")

settings = Settings()

openapi_tags = [
    {"name": "health", "description": "Healthcheck and environment info"},
    {"name": "classification", "description": "Image classification endpoints"},
    {"name": "detection", "description": "Image object detection endpoints"},
    {"name": "video", "description": "Video detection endpoints"},
    {"name": "websocket", "description": "WebSocket endpoints for real-time updates"},
]

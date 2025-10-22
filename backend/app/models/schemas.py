from typing import List, Optional
from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error detail message")

class Prediction(BaseModel):
    label: str = Field(..., description="Class label")
    score: float = Field(..., description="Confidence score [0-1]")

class ClassificationResponse(BaseModel):
    status: str = Field(..., description="Request status")
    elapsed: float = Field(..., description="Elapsed time in seconds")
    model: str = Field(..., description="Model used")
    device: str = Field(..., description="Device used for inference (cpu/cuda)")
    top_k: int = Field(..., description="Number of predictions returned")
    predictions: List[Prediction] = Field(..., description="Top-k predictions")
    upload_path: str = Field(..., description="Static path to the uploaded image")
    message: Optional[str] = Field(None, description="Additional information")

class Box(BaseModel):
    xmin: float = Field(..., description="Normalized left")
    ymin: float = Field(..., description="Normalized top")
    xmax: float = Field(..., description="Normalized right")
    ymax: float = Field(..., description="Normalized bottom")

class Detection(BaseModel):
    label: str = Field(..., description="Detected class")
    score: float = Field(..., description="Confidence score [0-1]")
    box: Box = Field(..., description="Bounding box in normalized coordinates")

class DetectionResponse(BaseModel):
    status: str = Field(..., description="Request status")
    elapsed: float = Field(..., description="Elapsed time in seconds")
    model: str = Field(..., description="Model used")
    device: str = Field(..., description="Device used for inference")
    detections: List[Detection] = Field(..., description="Detections list")
    upload_path: str = Field(..., description="Static path to the uploaded image")
    output_path: str = Field(..., description="Static path to the annotated output image")
    message: Optional[str] = Field(None, description="Additional information")

class VideoJobResponse(BaseModel):
    status: str = Field(..., description="Job status")
    elapsed: float = Field(..., description="Elapsed time in seconds")
    job_id: str = Field(..., description="Unique job identifier")
    upload_path: str = Field(..., description="Static path to the uploaded video")
    output_path: Optional[str] = Field(None, description="Static path to the processed video (when done)")
    message: Optional[str] = Field(None, description="Additional information")

class VideoStatusResponse(BaseModel):
    status: str = Field(..., description="Job status")
    progress: int = Field(..., description="Progress percent")
    job_id: str = Field(..., description="Unique job identifier")
    upload_path: str = Field(..., description="Static path to the uploaded video")
    output_path: Optional[str] = Field(None, description="Static path to the processed video if completed")
    message: Optional[str] = Field(None, description="Additional information")

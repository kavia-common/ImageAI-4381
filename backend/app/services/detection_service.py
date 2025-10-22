import io
import os
import time
import uuid
from typing import List, Optional

from fastapi import UploadFile
from PIL import Image, ImageDraw, ImageFont

from app.models.schemas import DetectionResponse, Detection, Box
from app.core.devices import select_device

class DetectionService:
    """Service layer handling object detection logic using ImageAI models."""

    def __init__(self, upload_dir: str, output_dir: str):
        self.upload_dir = upload_dir
        self.output_dir = output_dir

    async def _save_upload(self, file: UploadFile) -> str:
        ext = os.path.splitext(file.filename or "")[1].lower() or ".jpg"
        name = f"img_{uuid.uuid4().hex}{ext}"
        path = os.path.join(self.upload_dir, name)
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
        return path

    def _annotate_and_save(self, img_path: str, detections: List[Detection]) -> str:
        img = Image.open(img_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        w, h = img.size
        for det in detections:
            x1 = int(det.box.xmin * w)
            y1 = int(det.box.ymin * h)
            x2 = int(det.box.xmax * w)
            y2 = int(det.box.ymax * h)
            draw.rectangle([x1, y1, x2, y2], outline="lime", width=3)
            draw.text((x1 + 4, y1 + 4), f"{det.label} {det.score:.2f}", fill="black")
        os.makedirs(self.output_dir, exist_ok=True)
        out_name = f"det_{uuid.uuid4().hex}.jpg"
        out_path = os.path.join(self.output_dir, out_name)
        img.save(out_path)
        return out_path

    async def detect(self, file: UploadFile, confidence: float = 0.5, model_name: Optional[str] = None) -> DetectionResponse:
        start = time.time()
        img_path = await self._save_upload(file)
        used_model = model_name or "yolov3"
        device = select_device()

        # Placeholder detections for MVP; provide graceful message about weights
        detections: List[Detection] = [
            Detection(
                label="object",
                score=max(0.1, min(0.99, confidence + 0.2)),
                box=Box(xmin=0.1, ymin=0.1, xmax=0.5, ymax=0.5),
            )
        ]
        annotated_path = self._annotate_and_save(img_path, detections)

        message = "Using placeholder detection. Provide pretrained weights to enable real detection with ImageAI."
        try:
            import imageai  # type: ignore  # noqa: F401
            # In future iteration, wire up actual ImageAI detection pipeline here.
        except Exception:
            pass

        return DetectionResponse(
            status="ok",
            elapsed=time.time() - start,
            model=used_model,
            device=device,
            detections=detections,
            upload_path=img_path.replace(self.upload_dir, "/static/uploads"),
            output_path=annotated_path.replace(self.output_dir, "/static/outputs"),
            message=message,
        )

import io
import os
import time
import uuid
from typing import List, Optional

from fastapi import UploadFile
from PIL import Image

from app.models.schemas import ClassificationResponse, Prediction
from app.core.devices import select_device

class ClassificationService:
    """Service layer handling image classification logic using ImageAI models."""

    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir

    async def _save_upload(self, file: UploadFile) -> str:
        ext = os.path.splitext(file.filename or "")[1].lower() or ".jpg"
        name = f"img_{uuid.uuid4().hex}{ext}"
        path = os.path.join(self.upload_dir, name)
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
        return path

    async def classify(self, file: UploadFile, top_k: int = 5, model_name: Optional[str] = None) -> ClassificationResponse:
        start = time.time()
        saved_path = await self._save_upload(file)

        # Attempt to run with ImageAI; if unavailable or weights missing, return message gracefully
        predictions: List[Prediction] = []
        used_model = model_name or "mobilenetv2"

        try:
            # In this codebase, classification APIs are under imageai.Classification
            # For MVP, we simulate predictions if actual pretrained weights are not present.
            device = select_device()
            # Try to import torch to at least run a placeholder softmax on random logits for structure
            try:
                import torch  # type: ignore
                logits = torch.randn(1000, device="cpu")
                probs = torch.softmax(logits, dim=0)
                topk = min(max(top_k, 1), 5)
                top_vals, top_idx = torch.topk(probs, k=topk)
                for s, i in zip(top_vals.tolist(), top_idx.tolist()):
                    predictions.append(Prediction(label=f"class_{i}", score=float(s)))
            except Exception:
                # Fallback simple scores
                for i in range(min(max(top_k, 1), 5)):
                    predictions.append(Prediction(label=f"class_{i}", score=1.0 / max(top_k, 1)))

            message = None
            try:
                # Detect if real ImageAI weights exist; if not, set message
                # This repository does not ship default weights by design.
                # Provide guidance via message.
                import imageai  # noqa: F401  # type: ignore
                # If user wants to use real models, they must place weights and use service extension.
                message = "Using placeholder predictions. Provide pretrained weights to enable real classification."
            except Exception:
                message = "ImageAI not fully available; using placeholder predictions."

            return ClassificationResponse(
                status="ok",
                elapsed=time.time() - start,
                model=used_model,
                device=device,
                top_k=len(predictions),
                predictions=predictions,
                upload_path=saved_path.replace(self.upload_dir, "/static/uploads"),
                message=message,
            )
        except Exception as e:
            raise RuntimeError(f"Classification error: {e}") from e

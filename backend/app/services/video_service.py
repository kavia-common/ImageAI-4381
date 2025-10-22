import asyncio
import os
import time
import uuid
from typing import Dict, Optional

from fastapi import UploadFile

from app.models.schemas import VideoJobResponse, VideoStatusResponse
from app.core.devices import select_device

class VideoService:
    """Service layer for video detection jobs. Uses in-memory job tracking and simulated processing."""

    def __init__(self, upload_dir: str, output_dir: str, ws_manager):
        self.upload_dir = upload_dir
        self.output_dir = output_dir
        self.ws_manager = ws_manager
        self.jobs: Dict[str, Dict] = {}

    async def _save_upload(self, file: UploadFile) -> str:
        ext = os.path.splitext(file.filename or "")[1].lower() or ".mp4"
        name = f"vid_{uuid.uuid4().hex}{ext}"
        path = os.path.join(self.upload_dir, name)
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
        return path

    async def start_job(self, file: UploadFile, confidence: float = 0.5, model_name: Optional[str] = None) -> VideoJobResponse:
        job_id = uuid.uuid4().hex
        video_path = await self._save_upload(file)
        out_name = f"vidout_{job_id}.mp4"
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, out_name)

        self.jobs[job_id] = {
            "status": "queued",
            "progress": 0,
            "upload_path": video_path,
            "output_path": output_path,
            "model": model_name or "yolov3",
            "device": select_device(),
            "message": "Job queued",
            "started_at": time.time(),
            "completed_at": None,
        }

        # Start background task (simulate processing)
        asyncio.create_task(self._process_job(job_id, confidence))

        return VideoJobResponse(
            status="queued",
            elapsed=0.0,
            job_id=job_id,
            upload_path=video_path.replace(self.upload_dir, "/static/uploads"),
            output_path=None,
            message="Video detection started",
        )

    async def _process_job(self, job_id: str, confidence: float):
        job = self.jobs[job_id]
        job["status"] = "running"
        await self.ws_manager.broadcast(job_id, {"event": "started", "progress": 0, "status": "running"})

        # Simulate progress in steps, broadcasting updates
        for p in range(1, 101, 10):
            await asyncio.sleep(0.5)
            job["progress"] = p
            await self.ws_manager.broadcast(job_id, {"event": "progress", "progress": p, "status": "running"})

        # Simulate output creation by copying original file to output path
        try:
            import shutil
            shutil.copy(job["upload_path"], job["output_path"])
        except Exception:
            with open(job["output_path"], "wb") as f:
                f.write(b"")

        job["status"] = "completed"
        job["completed_at"] = time.time()
        job["message"] = "Completed (placeholder output). Provide weights to enable real processing."
        await self.ws_manager.broadcast(job_id, {"event": "completed", "progress": 100, "status": "completed", "output_path": job["output_path"].replace(self.output_dir, "/static/outputs")})

    async def status(self, job_id: str) -> VideoStatusResponse:
        if job_id not in self.jobs:
            raise KeyError(f"Job {job_id} not found")
        job = self.jobs[job_id]
        return VideoStatusResponse(
            status=job["status"],
            progress=job["progress"],
            job_id=job_id,
            upload_path=job["upload_path"].replace(self.upload_dir, "/static/uploads"),
            output_path=(job["output_path"].replace(self.output_dir, "/static/outputs") if job["status"] == "completed" else None),
            message=job["message"],
        )

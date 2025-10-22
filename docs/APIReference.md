# API Reference

## Overview
This document describes the HTTP API provided by the FastAPI backend and the WebSocket events used by the React frontend. It also summarizes request/response JSON schemas, error shapes, supported model names, device handling, file paths, and integration notes for the frontend API client.

- Local development URLs:
  - Backend: http://localhost:8000
  - Frontend: http://localhost:5173
  - OpenAPI: http://localhost:8000/docs
- Docker Compose service URLs (inside Docker network):
  - Backend: http://backend:8000
  - Frontend: http://frontend:5173

Static file serving:
- Static base: /static mounted to backend/app/data
- Uploads: /static/uploads
- Outputs: /static/outputs

## CORS and Environment
- CORS allowed origins are controlled by ALLOW_ORIGINS (comma-separated). Default: http://localhost:5173
- Model directory is controlled by MODEL_DIR. Default: /app/app/data/models
- Frontend uses VITE_API_BASE_URL for API base; defaults to http://backend:8000 in Compose and http://localhost:8000 in local dev.

## REST Endpoints

### GET /api/v1/health
- Summary: Health check and environment info.
- Request: No body.
- Response 200 application/json:
  - status: "ok"
  - elapsed: number
  - device: { cpu: boolean, cuda: boolean, cuda_device_count: number, device_preference: "cpu" | "cuda" }
  - versions: { fastapi: string, pydantic: string, python: string, opencv: string, torch: string, pillow: string, imageai: string }
  - static: { uploads: string, outputs: string }

### POST /api/v1/classify
- Summary: Classify an image.
- Consumes: multipart/form-data
- Form fields:
  - file: file (required)
  - top_k: integer (default 5)
  - model_name: string (optional)
- Response 200 application/json (ClassificationResponse):
  - status: string
  - elapsed: number
  - model: string
  - device: "cpu" | "cuda"
  - top_k: integer
  - predictions: Array<{ label: string, score: number }>
  - upload_path: string (e.g., "/static/uploads/...")
  - message?: string
- Errors:
  - 400 ErrorResponse { detail: string }
  - 500 ErrorResponse { detail: string }

### POST /api/v1/detect
- Summary: Detect objects in an image and save annotated output.
- Consumes: multipart/form-data
- Form fields:
  - file: file (required)
  - model_name: string (optional)
  - confidence: number in [0,1] (default 0.5)
- Response 200 application/json (DetectionResponse):
  - status: string
  - elapsed: number
  - model: string
  - device: "cpu" | "cuda"
  - detections: Array<{
      label: string,
      score: number,
      box: { xmin: number, ymin: number, xmax: number, ymax: number }  // normalized [0..1]
    }>
  - upload_path: string ("/static/uploads/...")
  - output_path: string ("/static/outputs/...")
  - message?: string
- Errors:
  - 400 ErrorResponse { detail: string }
  - 500 ErrorResponse { detail: string }

### POST /api/v1/video/detect
- Summary: Start a video detection job (background processing).
- Consumes: multipart/form-data
- Form fields:
  - file: file (required)
  - model_name: string (optional)
  - confidence: number in [0,1] (default 0.5)
- Response 200 application/json (VideoJobResponse):
  - status: string
  - elapsed: number
  - job_id: string
  - upload_path: string ("/static/uploads/...")
  - output_path?: string ( may be null/undefined until completed )
  - message?: string
- Errors:
  - 400 ErrorResponse { detail: string }
  - 500 ErrorResponse { detail: string }

### GET /api/v1/video/status/{job_id}
- Summary: Get video job status.
- Path params:
  - job_id: string
- Response 200 application/json (VideoStatusResponse):
  - status: string
  - progress: number (0..100)
  - job_id: string
  - upload_path: string
  - output_path?: string
  - message?: string
- Errors:
  - 404 ErrorResponse { detail: string }

## WebSocket Endpoint

### WS /ws/video/{job_id}
- Summary: Subscribe to progress updates for a video detection job.
- Protocol: ws:// or wss:// depending on base URL.
- Client behavior: Keep connection open; server pushes JSON events. The server expects occasional ping (client may send keep-alive text to avoid timeouts).

Event payloads:
- Progress event:
  { "type": "progress", "progress": number, "frame": number, "total_frames": number }
- Completion event:
  { "type": "complete", "output_path": string, "message"?: string }
- Error event:
  { "type": "error", "message": string }

Note: Exact fields of WS messages originate from the video service via ws_manager.broadcast(job_id, payload). The formats above are recommended for clients; confirm against emitted payloads during development.

## JSON Schemas (Pydantic models)

- ErrorResponse
  - detail: string

- Prediction
  - label: string
  - score: number

- ClassificationResponse
  - status: string
  - elapsed: number
  - model: string
  - device: string
  - top_k: number
  - predictions: Prediction[]
  - upload_path: string
  - message?: string

- Box
  - xmin: number
  - ymin: number
  - xmax: number
  - ymax: number

- Detection
  - label: string
  - score: number
  - box: Box

- DetectionResponse
  - status: string
  - elapsed: number
  - model: string
  - device: string
  - detections: Detection[]
  - upload_path: string
  - output_path: string
  - message?: string

- VideoJobResponse
  - status: string
  - elapsed: number
  - job_id: string
  - upload_path: string
  - output_path?: string
  - message?: string

- VideoStatusResponse
  - status: string
  - progress: number
  - job_id: string
  - upload_path: string
  - output_path?: string
  - message?: string

## Model Names and Device Handling
- Model names accepted by endpoints are optional; when provided, they should match the service implementation. In absence of a value, defaults in services are used.
- Device selection is automatic:
  - If torch.cuda.is_available() then device "cuda"
  - Otherwise device "cpu"
- Device info endpoint: GET /api/v1/health returns gpu availability and device counts.

## File Handling and Paths
- Uploads are saved to backend/app/data/uploads and exposed via /static/uploads.
- Outputs (annotated images/videos) are saved to backend/app/data/outputs and exposed via /static/outputs.
- Use the returned upload_path/output_path URLs directly in the frontend for previews and downloads.

## Frontend Integration Notes
- API base URL: getApiBaseUrl() in frontend/src/config.ts reads import.meta.env.VITE_API_BASE_URL.
  - Local dev: export VITE_API_BASE_URL=http://localhost:8000
  - Docker Compose: default http://backend:8000
- Axios client: frontend/src/api/client.ts uses baseURL=getApiBaseUrl().
- Implemented client methods:
  - getHealth(): GET /api/v1/health
  - classifyImage(file): POST /api/v1/classify
  - detectObjects(file): POST /api/v1/detect
  - startVideoDetection(file): should call POST /api/v1/video/detect
  - openVideoWs(jobId): connects to {wsBase}/ws/video/{job_id}
- WebSocket base URL is derived from API base via getWsBaseUrl().

Important: Align frontend route for video start with backend
- Backend provides POST /api/v1/video/detect
- If the frontend currently calls /api/v1/video/start, update it to /api/v1/video/detect or add a backend alias.

## Error Shape
- All errors are returned as JSON:
  { "detail": string }
- HTTP codes used:
  - 400: validation or bad request (e.g., missing/invalid form fields)
  - 404: job not found
  - 500: internal error during processing

## Example cURL

- Classification
  curl -X POST -F "file=@test-images/1.jpg" -F "top_k=5" http://localhost:8000/api/v1/classify

- Detection
  curl -X POST -F "file=@test-images/2.jpg" -F "confidence=0.5" http://localhost:8000/api/v1/detect

- Start Video
  curl -X POST -F "file=@data-videos/traffic-mini.mp4" -F "confidence=0.5" http://localhost:8000/api/v1/video/detect

- Video Status
  curl http://localhost:8000/api/v1/video/status/<job_id>

- WebSocket (example JS)
  const ws = new WebSocket("ws://localhost:8000/ws/video/<job_id>");
  ws.onmessage = (e) => console.log(JSON.parse(e.data));


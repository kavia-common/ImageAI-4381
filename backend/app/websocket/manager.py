from typing import Dict, List
from fastapi import WebSocket

class WebSocketManager:
    """Manages WebSocket connections grouped by job_id."""

    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, job_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections.setdefault(job_id, []).append(websocket)

    def disconnect(self, job_id: str, websocket: WebSocket):
        conns = self.connections.get(job_id, [])
        if websocket in conns:
            conns.remove(websocket)

    async def broadcast(self, job_id: str, message: dict):
        for ws in list(self.connections.get(job_id, [])):
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(job_id, ws)

ws_manager = WebSocketManager()

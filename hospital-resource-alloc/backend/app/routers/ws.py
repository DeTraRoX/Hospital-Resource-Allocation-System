# backend/app/routers/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        async with self.lock:
            connections = list(self.active_connections)

        if not connections:
            return

        await asyncio.gather(
            *[ws.send_text(message) for ws in connections],
            return_exceptions=True
        )

manager = ConnectionManager()

@router.websocket("/ws/resources")
async def websocket_resources(ws: WebSocket):
    """WebSocket endpoint for dashboards to receive real-time updates."""
    await manager.connect(ws)
    try:
        while True:
            # Optional: receive pings from clients to keep alive
            await ws.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(ws)

# Helper function other routers can call
async def broadcast_update(summary: dict):
    """Broadcast a new resource summary to all dashboards."""
    payload = {
        "type": "resource_update",
        "summary": summary
    }
    await manager.broadcast(json.dumps(payload))
async def broadcast_active_patients(patients: list):
    """Send updated active patients list to all dashboards"""
    payload = {
        "type": "active_patients",
        "patients": patients
    }
    await manager.broadcast(json.dumps(payload))

async def broadcast_waiting_patients(patients: list):
    """Send updated waiting patients list to all dashboards"""
    payload = {
        "type": "waiting_patients",
        "patients": patients
    }
    await manager.broadcast(json.dumps(payload))
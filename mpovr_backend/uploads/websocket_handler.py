import json
from fastapi import WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, auth, schemas
from .database import get_db

async def get_current_user_ws(
    websocket: WebSocket,
    token: str,
    db: Session = Depends(get_db)
):
    try:
        current_user = await auth.get_current_user(token, db)
        return current_user
    except HTTPException:
        await websocket.close(code=1008)  # Policy Violation
        return None

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, program_id: int):
        await websocket.accept()
        if program_id not in self.active_connections:
            self.active_connections[program_id] = []
        self.active_connections[program_id].append(websocket)

    def disconnect(self, websocket: WebSocket, program_id: int):
        if program_id in self.active_connections:
            self.active_connections[program_id] = [
                conn for conn in self.active_connections[program_id] if conn != websocket
            ]
            if not self.active_connections[program_id]:
                del self.active_connections[program_id]

    async def broadcast(self, content: dict, program_id: int):
        print('Broadcasting:', content)
        print('Active connections:', self.active_connections)
        print('Program ID:', program_id)
        if program_id in self.active_connections:
            for connection in self.active_connections[program_id]:
                await connection.send_json(content)

manager = ConnectionManager()

async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    db: Session = Depends(get_db)
):
    current_user = await get_current_user_ws(websocket, token, db)
    if not current_user:
        return

    program_id = crud.get_user_program_id(db, current_user.user_id)
    if not program_id:
        await websocket.close(code=1008)  # Policy Violation
        return

    await manager.connect(websocket, program_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Process received data if needed
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        manager.disconnect(websocket, program_id)

async def broadcast_content(content: dict, program_id: int):
    print('Broadcasting:', content)
    await manager.broadcast(content, program_id)


import json
import asyncio
import logging
from fastapi import WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, auth, schemas
from .database import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info(f"New connection added. Total connections for program {program_id}: {len(self.active_connections[program_id])}")

    def disconnect(self, websocket: WebSocket, program_id: int):
        if program_id in self.active_connections:
            self.active_connections[program_id] = [
                conn for conn in self.active_connections[program_id] if conn != websocket
            ]
            logger.info(f"Connection removed. Total connections for program {program_id}: {len(self.active_connections[program_id])}")
            if not self.active_connections[program_id]:
                del self.active_connections[program_id]
                logger.info(f"No more connections for program {program_id}. Removed from active_connections.")

    async def broadcast(self, content: dict, program_id: int):
        logger.info(f'Broadcasting to program {program_id}. Active connections: {len(self.active_connections.get(program_id, []))}')
        if program_id in self.active_connections:
            for connection in self.active_connections[program_id]:
                try:
                    await connection.send_json(content)
                except Exception as e:
                    logger.error(f"Error broadcasting to a connection: {str(e)}")
                    await self.disconnect(connection, program_id)

manager = ConnectionManager()

async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    db: Session = Depends(get_db)
):
    current_user = await get_current_user_ws(websocket, token, db)
    if not current_user:
        logger.warning(f"WebSocket connection attempt with invalid token")
        return

    program_id = crud.get_user_program_id(db, current_user.user_id)
    if not program_id:
        logger.warning(f"User {current_user.user_id} not associated with any program")
        await websocket.close(code=1008)  # Policy Violation
        return

    await manager.connect(websocket, program_id)
    logger.info(f"WebSocket connection established for user {current_user.user_id} in program {program_id}")

    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                if data == "pong":
                    continue
                # Process received data if needed
                logger.info(f"Received data from user {current_user.user_id}: {data}")
            except asyncio.TimeoutError:
                await websocket.send_text('ping')
            except Exception as e:
                logger.error(f"Error processing WebSocket data: {str(e)}")
                break
    except Exception as e:
        logger.error(f"WebSocket error for user {current_user.user_id}: {str(e)}")
    finally:
        logger.info(f"WebSocket disconnected for user {current_user.user_id} in program {program_id}")
        manager.disconnect(websocket, program_id)

async def broadcast_content(content: dict, program_id: int):
    logger.info(f'Broadcasting content to program {program_id}: {json.dumps(content)}')
    await manager.broadcast(content, program_id)
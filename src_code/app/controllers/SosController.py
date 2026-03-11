from fastapi import WebSocket, WebSocketDisconnect
from app.websocket.ConnectionManager import manager


async def sos_socket(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
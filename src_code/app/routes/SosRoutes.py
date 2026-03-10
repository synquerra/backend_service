from fastapi import APIRouter, WebSocket
from app.controllers.SosController import sos_socket

router = APIRouter()

@router.websocket("/ws/sos_notification")
async def websocket_endpoint(websocket: WebSocket):
    await sos_socket(websocket)
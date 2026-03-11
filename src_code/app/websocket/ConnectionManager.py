from typing import List
from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

        print("WebSocket connected. Total:", len(self.active_connections))

        await websocket.send_json({
            "event": "CONNECTED",
            "message": "SOS notification websocket connected successfully"
        })

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print("WebSocket disconnected. Total:", len(self.active_connections))

    async def broadcast(self, message: dict):

        print("Broadcasting message:", message)
        print("Active connections:", len(self.active_connections))

        dead_connections = []

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print("WebSocket send failed:", e)
                dead_connections.append(connection)

        for conn in dead_connections:
            self.disconnect(conn)


manager = ConnectionManager()
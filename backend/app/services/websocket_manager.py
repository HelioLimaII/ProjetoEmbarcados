from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # Lista de conexões ativas (abas do navegador abertas)
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Envia a mensagem para todos os navegadores conectados
        for connection in self.active_connections:
            await connection.send_json(message)

# Instância única para ser usada em toda a aplicação
manager = ConnectionManager()
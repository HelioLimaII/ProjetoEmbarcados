from fastapi import FastAPI
from app.routers import scan, products
from fastapi import WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager

app = FastAPI(
    title="EstoqueManager API",
    description="API para gerenciamento de estoque via QR Code Scanner",
    version="1.0.0"
)

# Registra as rotas da aplicação
app.include_router(scan.router)
app.include_router(products.router) # <-- Adicionamos esta linha!

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "EstoqueManager API is running no M1!"}

@app.websocket("/ws/scans")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Mantém a conexão viva esperando mensagens (embora só o server vá enviar)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import scan, products
from app.services.websocket_manager import manager

app = FastAPI(
    title="EstoqueManager API",
    description="API para gerenciamento de estoque via QR Code Scanner",
    version="1.0.0"
)

# 1. Configuração do CORS (Isso resolve o erro 403 Forbidden!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que o Front-end conecte sem ser bloqueado
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas da aplicação
app.include_router(scan.router)
app.include_router(products.router)

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "EstoqueManager API is running no M1!"}

# 2. Rota ajustada de /ws/scans para /ws para bater com o código do Next.js
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Mantém a conexão viva esperando mensagens
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
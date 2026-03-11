from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.qr_service import process_image_and_decode
from app.services import product_service
from app.services.websocket_manager import manager
from app.dependencies import get_api_key
from app.database import get_db

router = APIRouter(prefix="/api/v1/scan", tags=["Scan"])

@router.post("")
async def scan_qr_code(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
    db: AsyncSession = Depends(get_db)
):
    # Valida se é uma imagem aceita (JPEG ou PNG) conforme FR-04
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="O arquivo deve ser uma imagem JPEG ou PNG")
    
    # Lê o arquivo para a memória conforme FR-03 e FR-05
    file_bytes = await file.read()
    
    # Chama o serviço de decodificação pyzbar conforme FR-02
    qr_data = await process_image_and_decode(file_bytes)
    
    # Retorna o formato exigido na US-001
    if qr_data:
        # Busca o produto associado ao QR Code no PostgreSQL
        product = await product_service.get_product_by_qr(db, qr_data)
        
        if product:
            # Notifica a interface Web em tempo real via WebSocket
            await manager.broadcast({
                "event": "PRODUCT_SCANNED",
                "product": {
                    "id": str(product.id),
                    "name": product.name,
                    "qr_code": product.qr_code,
                    "quantity": product.quantity,
                    "category": product.category
                }
            })
            return {
                "code": qr_data, 
                "found": True, 
                "product_name": product.name,
                "message": "Produto identificado e enviado para o dashboard"
            }
        
        # QR detectado, mas não está no cadastro
        return {
            "code": qr_data, 
            "found": True, 
            "product": None, 
            "message": "QR Code válido, mas produto não cadastrado"
        }
    
    # Nenhum QR Code encontrado na imagem
    return {"code": None, "found": False, "message": "QR Code não detectado"}
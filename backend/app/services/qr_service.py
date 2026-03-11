import io
from PIL import Image
from pyzbar.pyzbar import decode, ZBarSymbol

async def process_image_and_decode(file_bytes: bytes) -> str | None:
    try:
        # Carrega a imagem na memória usando Pillow (FR-05)
        image = Image.open(io.BytesIO(file_bytes))
        
        # Decodifica usando pyzbar (FR-02)
        # Filtramos apenas para QRCODE para processar mais rápido (<500ms)
        decoded_objects = decode(image, symbols=[ZBarSymbol.QRCODE])
        
        if decoded_objects:
            # Retorna o texto decodificado do primeiro QR Code encontrado
            return decoded_objects[0].data.decode("utf-8")
        
        return None
    except Exception as e:
        print(f"Erro ao decodificar imagem: {e}")
        return None
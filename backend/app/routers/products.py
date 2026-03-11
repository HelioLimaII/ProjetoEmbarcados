from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database import get_db
from app.dependencies import get_api_key
from app.schemas.product import ProductCreate, ProductResponse
from app.services import product_service

# Define o prefixo e as tags para organizar o Swagger
router = APIRouter(prefix="/api/v1/products", tags=["Products"])

# Rota para criar um produto (US-003)
@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    # Verifica se o QR Code já existe no banco para evitar duplicatas
    existing_product = await product_service.get_product_by_qr(db, product.qr_code)
    if existing_product:
        raise HTTPException(status_code=409, detail="Já existe um produto com este QR Code cadastrado")
    
    return await product_service.create_product(db, product)

# Rota para listar produtos (US-004)
@router.get("", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0, 
    limit: int = 20, 
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    return await product_service.list_products(db, skip=skip, limit=limit)

# Rota para buscar produto direto pelo QR Code (US-008)
@router.get("/by-qr/{qr_code}", response_model=ProductResponse)
async def get_product_by_qr_code(
    qr_code: str, 
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    product = await product_service.get_product_by_qr(db, qr_code)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_stock(
    product_id: UUID,
    quantity_change: int, # Enviamos -1 para venda/uso
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    product = await product_service.update_product_stock(db, product_id, quantity_change)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product
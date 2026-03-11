from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

# Cria um novo produto no banco (US-003)
async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Busca um produto pelo QR Code (US-002 e US-008)
async def get_product_by_qr(db: AsyncSession, qr_code: str) -> Product | None:
    result = await db.execute(select(Product).filter(Product.qr_code == qr_code))
    return result.scalars().first()

# Busca um produto pelo ID (US-005)
async def get_product_by_id(db: AsyncSession, product_id: UUID) -> Product | None:
    result = await db.execute(select(Product).filter(Product.id == product_id))
    return result.scalars().first()

# Retorna uma lista de produtos (US-004)
async def list_products(db: AsyncSession, skip: int = 0, limit: int = 20):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()

async def update_product_stock(db: AsyncSession, product_id: UUID, quantity_change: int) -> Product | None:
    product = await get_product_by_id(db, product_id)
    if product:
        # Decrementa a quantidade (ex: 5 + (-1) = 4)
        product.quantity += quantity_change
        
        # Garante que o estoque não fique negativo
        if product.quantity < 0:
            product.quantity = 0
            
        await db.commit()
        await db.refresh(product)
    return product
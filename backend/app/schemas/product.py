from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

# Base com os campos comuns
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    qr_code: str
    category: Optional[str] = None
    quantity: int = 0
    price: Optional[Decimal] = None
    location: Optional[str] = None

# Schema para criação (US-003)
class ProductCreate(ProductBase):
    pass

# Schema para atualização parcial (US-006)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    qr_code: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[Decimal] = None
    location: Optional[str] = None

# Schema de resposta (o que a API devolve)
class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    # Permite que o Pydantic leia dados direto dos modelos do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
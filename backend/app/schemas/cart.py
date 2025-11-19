"""
Pydantic schemas for Cart API
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class CartItemBase(BaseModel):
    variant_id: int
    quantity: int = Field(..., ge=1)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItem(CartItemBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CartItemWithProduct(CartItem):
    """Cart item with product details for display"""
    variant_name: str
    variant_sku: str
    product_name: str
    product_slug: str
    price: Decimal
    image_url: Optional[str] = None
    stock_available: int

    class Config:
        from_attributes = True


class CartSummary(BaseModel):
    """Summary of cart contents"""
    items: list[CartItemWithProduct]
    total_items: int
    subtotal: Decimal
    estimated_tax: Decimal
    estimated_total: Decimal

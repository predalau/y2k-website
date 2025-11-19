"""
Pydantic schemas for Order API
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class OrderItemBase(BaseModel):
    variant_id: int
    quantity: int = Field(..., ge=1)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(BaseModel):
    id: int
    order_id: int
    variant_id: int
    artist_id: Optional[int]
    product_name: str
    variant_name: str
    sku: str
    price: Decimal
    quantity: int
    subtotal: Decimal
    artist_commission_rate: Optional[Decimal]
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    shipping_address_id: Optional[int] = None
    billing_address_id: Optional[int] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Create order from cart or direct checkout"""
    items: List[OrderItemCreate] = []


class OrderUpdate(BaseModel):
    """Update order (admin only)"""
    status: Optional[str] = Field(None, pattern="^(pending|paid|processing|shipped|delivered|cancelled|refunded)$")
    tracking_number: Optional[str] = None
    admin_notes: Optional[str] = None


class Order(OrderBase):
    id: int
    user_id: int
    order_number: str
    status: str
    subtotal: Decimal
    tax_amount: Decimal
    shipping_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    currency: str
    customer_email: str
    customer_phone: Optional[str]
    tracking_number: Optional[str]
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class OrderWithItems(Order):
    """Order with all items"""
    order_items: List[OrderItem] = []

    class Config:
        from_attributes = True


class OrderList(BaseModel):
    """Minimal order info for list views"""
    id: int
    order_number: str
    status: str
    total_amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True

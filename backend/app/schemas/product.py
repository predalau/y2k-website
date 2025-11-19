"""
Pydantic schemas for Product, ProductVariant, and ProductImage API
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# Product Image Schemas
class ProductImageBase(BaseModel):
    image_url: str = Field(..., max_length=500)
    alt_text: Optional[str] = Field(None, max_length=255)
    display_order: int = 0
    is_primary: bool = False


class ProductImageCreate(ProductImageBase):
    pass


class ProductImage(ProductImageBase):
    id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Product Variant Schemas
class ProductVariantBase(BaseModel):
    sku: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    size: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=100)
    style: Optional[str] = Field(None, max_length=100)
    price: Decimal = Field(..., ge=0)
    compare_at_price: Optional[Decimal] = Field(None, ge=0)
    cost: Optional[Decimal] = Field(None, ge=0)
    weight: Optional[Decimal] = Field(None, ge=0)
    requires_shipping: bool = True
    stock_quantity: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=5, ge=0)
    track_inventory: bool = True
    is_active: bool = True
    display_order: int = 0


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantUpdate(BaseModel):
    """All fields optional for updates"""
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    size: Optional[str] = None
    color: Optional[str] = None
    style: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    compare_at_price: Optional[Decimal] = Field(None, ge=0)
    cost: Optional[Decimal] = Field(None, ge=0)
    weight: Optional[Decimal] = Field(None, ge=0)
    requires_shipping: Optional[bool] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)
    track_inventory: Optional[bool] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class ProductVariant(ProductVariantBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    short_description: Optional[str] = Field(None, max_length=500)
    product_type: str = Field(..., pattern="^(physical|digital|both)$")
    digital_file_url: Optional[str] = Field(None, max_length=500)
    base_price: Decimal = Field(..., ge=0)
    is_active: bool = True
    featured: bool = False


class ProductCreate(ProductBase):
    artist_id: int
    category_id: Optional[int] = None
    variants: Optional[List[ProductVariantCreate]] = []
    images: Optional[List[ProductImageCreate]] = []


class ProductUpdate(BaseModel):
    """All fields optional for updates"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    short_description: Optional[str] = None
    product_type: Optional[str] = Field(None, pattern="^(physical|digital|both)$")
    digital_file_url: Optional[str] = None
    base_price: Optional[Decimal] = Field(None, ge=0)
    category_id: Optional[int] = None
    is_active: Optional[bool] = None
    featured: Optional[bool] = None


class Product(ProductBase):
    id: int
    artist_id: int
    category_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductWithDetails(Product):
    """Product with all related data"""
    variants: List[ProductVariant] = []
    images: List[ProductImage] = []
    # Can add artist and category here too if needed

    class Config:
        from_attributes = True


class ProductList(BaseModel):
    """Minimal product info for list views"""
    id: int
    name: str
    slug: str
    short_description: Optional[str]
    base_price: Decimal
    product_type: str
    is_active: bool
    featured: bool
    artist_id: int

    class Config:
        from_attributes = True

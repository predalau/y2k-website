"""
Pydantic schemas package
Import all schemas here for easy access
"""
from .user import User, UserCreate, UserUpdate, UserPublic, Token, TokenData, UserLogin
from .artist import Artist, ArtistCreate, ArtistUpdate, ArtistList
from .product import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductList,
    ProductWithDetails,
    ProductVariant,
    ProductVariantCreate,
    ProductVariantUpdate,
    ProductImage,
    ProductImageCreate,
)
from .cart import CartItem, CartItemCreate, CartItemUpdate, CartItemWithProduct, CartSummary
from .order import Order, OrderCreate, OrderUpdate, OrderWithItems, OrderList, OrderItem

__all__ = [
    # User schemas
    "User",
    "UserCreate",
    "UserUpdate",
    "UserPublic",
    "Token",
    "TokenData",
    "UserLogin",
    # Artist schemas
    "Artist",
    "ArtistCreate",
    "ArtistUpdate",
    "ArtistList",
    # Product schemas
    "Product",
    "ProductCreate",
    "ProductUpdate",
    "ProductList",
    "ProductWithDetails",
    "ProductVariant",
    "ProductVariantCreate",
    "ProductVariantUpdate",
    "ProductImage",
    "ProductImageCreate",
    # Cart schemas
    "CartItem",
    "CartItemCreate",
    "CartItemUpdate",
    "CartItemWithProduct",
    "CartSummary",
    # Order schemas
    "Order",
    "OrderCreate",
    "OrderUpdate",
    "OrderWithItems",
    "OrderList",
    "OrderItem",
]

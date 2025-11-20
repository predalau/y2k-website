"""
Cart routes for AEVVM store
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from decimal import Decimal

from app.database import get_db
from app.models.cart import Cart, CartItem
from app.models.product import ProductVariant

router = APIRouter()


class AddToCartRequest(BaseModel):
    variant_id: int
    quantity: int = 1


class UpdateCartItemRequest(BaseModel):
    quantity: int


@router.post("/")
def add_to_cart(
    request: AddToCartRequest,
    session_id: str,
    db: Session = Depends(get_db)
):
    """Add item to cart (guest cart using session_id)"""
    # Get or create cart for session
    cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    if not cart:
        cart = Cart(session_id=session_id)
        db.add(cart)
        db.flush()

    # Check if variant exists
    variant = db.query(ProductVariant).filter(ProductVariant.id == request.variant_id).first()
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")

    # Check if item already in cart
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.variant_id == request.variant_id
    ).first()

    if cart_item:
        # Update quantity
        cart_item.quantity += request.quantity
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            variant_id=request.variant_id,
            quantity=request.quantity,
            price=variant.price
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Item added to cart",
        "cart_item_id": cart_item.id,
        "quantity": cart_item.quantity
    }


@router.get("/")
def get_cart(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get cart contents"""
    cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    if not cart:
        return {"items": [], "total": 0, "item_count": 0}

    items = []
    total = Decimal('0.00')
    item_count = 0

    for cart_item in cart.items:
        variant = cart_item.variant
        product = variant.product
        item_total = cart_item.price * cart_item.quantity
        total += item_total
        item_count += cart_item.quantity

        items.append({
            "id": cart_item.id,
            "variant_id": variant.id,
            "product_id": product.id,
            "product_name": product.name,
            "variant_name": variant.name,
            "price": float(cart_item.price),
            "quantity": cart_item.quantity,
            "subtotal": float(item_total),
            "image_url": product.images[0].image_url if product.images else None
        })

    return {
        "items": items,
        "total": float(total),
        "item_count": item_count
    }


@router.put("/{cart_item_id}")
def update_cart_item(
    cart_item_id: int,
    request: UpdateCartItemRequest,
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if request.quantity <= 0:
        # Remove item if quantity is 0 or negative
        db.delete(cart_item)
    else:
        cart_item.quantity = request.quantity

    db.commit()

    return {"message": "Cart updated"}


@router.delete("/{cart_item_id}")
def remove_from_cart(
    cart_item_id: int,
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()

    return {"message": "Item removed from cart"}


@router.delete("/")
def clear_cart(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Clear all items from cart"""
    cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    if cart:
        for item in cart.items:
            db.delete(item)
        db.commit()

    return {"message": "Cart cleared"}

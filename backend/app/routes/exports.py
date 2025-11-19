"""
Data export routes (CSV, Excel) for admin dashboard
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import csv
import io

from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.product import Product, ProductVariant
from app.models.artist import Artist

router = APIRouter()


def generate_csv(headers: list, rows: list) -> StreamingResponse:
    """
    Helper function to generate CSV response
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"}
    )


@router.get("/orders")
def export_orders(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Export orders to CSV
    """
    query = db.query(Order)

    # Apply filters
    if start_date:
        query = query.filter(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Order.created_at <= datetime.fromisoformat(end_date))
    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc()).all()

    # CSV headers
    headers = [
        "Order Number", "Customer Email", "Customer Phone", "Status",
        "Subtotal", "Tax", "Shipping", "Discount", "Total",
        "Currency", "Created At", "Shipped At", "Tracking Number"
    ]

    # CSV rows
    rows = [
        [
            order.order_number,
            order.customer_email,
            order.customer_phone or "",
            order.status,
            float(order.subtotal),
            float(order.tax_amount),
            float(order.shipping_amount),
            float(order.discount_amount),
            float(order.total_amount),
            order.currency,
            order.created_at.isoformat(),
            order.shipped_at.isoformat() if order.shipped_at else "",
            order.tracking_number or ""
        ]
        for order in orders
    ]

    return generate_csv(headers, rows)


@router.get("/order-items")
def export_order_items(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Export order items (line items) to CSV
    """
    query = db.query(OrderItem).join(Order)

    if start_date:
        query = query.filter(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Order.created_at <= datetime.fromisoformat(end_date))

    items = query.order_by(Order.created_at.desc()).all()

    headers = [
        "Order Number", "Product Name", "Variant Name", "SKU",
        "Price", "Quantity", "Subtotal", "Artist Commission Rate",
        "Order Date"
    ]

    rows = []
    for item in items:
        order = db.query(Order).filter(Order.id == item.order_id).first()
        rows.append([
            order.order_number if order else "",
            item.product_name,
            item.variant_name,
            item.sku,
            float(item.price),
            item.quantity,
            float(item.subtotal),
            float(item.artist_commission_rate) if item.artist_commission_rate else "",
            order.created_at.isoformat() if order else ""
        ])

    return generate_csv(headers, rows)


@router.get("/users")
def export_users(
    is_active: Optional[bool] = None,
    email_verified: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Export users to CSV
    """
    query = db.query(User)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if email_verified is not None:
        query = query.filter(User.email_verified == email_verified)

    users = query.order_by(User.created_at.desc()).all()

    headers = [
        "ID", "Email", "Full Name", "Phone", "Is Active",
        "Is Admin", "Email Verified", "Created At"
    ]

    rows = [
        [
            user.id,
            user.email,
            user.full_name or "",
            user.phone or "",
            user.is_active,
            user.is_admin,
            user.email_verified,
            user.created_at.isoformat()
        ]
        for user in users
    ]

    return generate_csv(headers, rows)


@router.get("/products")
def export_products(
    is_active: Optional[bool] = None,
    artist_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Export products to CSV
    """
    query = db.query(Product)

    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    if artist_id:
        query = query.filter(Product.artist_id == artist_id)

    products = query.all()

    headers = [
        "ID", "Name", "Slug", "Artist ID", "Category ID",
        "Product Type", "Base Price", "Is Active", "Featured", "Created At"
    ]

    rows = [
        [
            product.id,
            product.name,
            product.slug,
            product.artist_id,
            product.category_id or "",
            product.product_type,
            float(product.base_price),
            product.is_active,
            product.featured,
            product.created_at.isoformat()
        ]
        for product in products
    ]

    return generate_csv(headers, rows)


@router.get("/inventory")
def export_inventory(
    low_stock_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Export product inventory to CSV
    """
    query = db.query(ProductVariant).filter(ProductVariant.track_inventory == True)

    if low_stock_only:
        query = query.filter(
            ProductVariant.stock_quantity <= ProductVariant.low_stock_threshold
        )

    variants = query.all()

    headers = [
        "Variant ID", "SKU", "Name", "Size", "Color", "Style",
        "Price", "Stock Quantity", "Low Stock Threshold", "Is Active"
    ]

    rows = [
        [
            variant.id,
            variant.sku,
            variant.name,
            variant.size or "",
            variant.color or "",
            variant.style or "",
            float(variant.price),
            variant.stock_quantity,
            variant.low_stock_threshold,
            variant.is_active
        ]
        for variant in variants
    ]

    return generate_csv(headers, rows)


@router.get("/artist-sales")
def export_artist_sales(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Export artist sales and commission data to CSV
    """
    from sqlalchemy import func

    query = db.query(
        Artist.id,
        Artist.name,
        func.sum(OrderItem.subtotal).label('total_revenue'),
        func.sum(OrderItem.quantity).label('total_items_sold'),
        func.avg(OrderItem.artist_commission_rate).label('avg_commission_rate')
    ).join(OrderItem, Artist.id == OrderItem.artist_id).join(Order)

    if start_date:
        query = query.filter(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Order.created_at <= datetime.fromisoformat(end_date))

    query = query.filter(
        Order.status.in_(['paid', 'processing', 'shipped', 'delivered'])
    ).group_by(Artist.id)

    results = query.all()

    headers = [
        "Artist ID", "Artist Name", "Total Revenue", "Items Sold",
        "Avg Commission Rate", "Estimated Commission"
    ]

    rows = [
        [
            r.id,
            r.name,
            float(r.total_revenue),
            r.total_items_sold,
            float(r.avg_commission_rate or 0),
            float(r.total_revenue * (r.avg_commission_rate or 0) / 100)
        ]
        for r in results
    ]

    return generate_csv(headers, rows)

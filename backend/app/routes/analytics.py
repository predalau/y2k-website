"""
Analytics API routes for admin dashboard
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional, List
from datetime import datetime, timedelta
from decimal import Decimal

from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.product import Product, ProductVariant
from app.models.artist import Artist

router = APIRouter()


@router.get("/dashboard-stats")
def get_dashboard_stats(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get high-level dashboard statistics
    - Total sales
    - Total orders
    - Total users
    - Average order value
    """
    # Parse dates
    date_filter = []
    if start_date:
        start = datetime.fromisoformat(start_date)
        date_filter.append(Order.created_at >= start)
    if end_date:
        end = datetime.fromisoformat(end_date)
        date_filter.append(Order.created_at <= end)

    # Total sales (completed orders only)
    total_sales = db.query(func.sum(Order.total_amount)).filter(
        Order.status.in_(['paid', 'processing', 'shipped', 'delivered']),
        *date_filter
    ).scalar() or Decimal('0.00')

    # Total orders
    total_orders = db.query(func.count(Order.id)).filter(*date_filter).scalar() or 0

    # Total users (all time)
    total_users = db.query(func.count(User.id)).scalar() or 0

    # Average order value
    avg_order_value = db.query(func.avg(Order.total_amount)).filter(
        Order.status.in_(['paid', 'processing', 'shipped', 'delivered']),
        *date_filter
    ).scalar() or Decimal('0.00')

    # New users in date range
    user_filter = []
    if start_date:
        user_filter.append(User.created_at >= start)
    if end_date:
        user_filter.append(User.created_at <= end)
    new_users = db.query(func.count(User.id)).filter(*user_filter).scalar() or 0

    return {
        "total_sales": float(total_sales),
        "total_orders": total_orders,
        "total_users": total_users,
        "new_users": new_users,
        "avg_order_value": float(avg_order_value),
        "date_range": {
            "start": start_date,
            "end": end_date
        }
    }


@router.get("/sales-over-time")
def get_sales_over_time(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = Query("day", pattern="^(day|week|month)$"),
    db: Session = Depends(get_db)
):
    """
    Get sales data grouped by time interval for charts
    Returns data points for line/bar charts
    """
    date_filter = []
    if start_date:
        date_filter.append(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        date_filter.append(Order.created_at <= datetime.fromisoformat(end_date))

    # Group by interval
    if interval == "day":
        time_group = func.date(Order.created_at)
    elif interval == "month":
        time_group = func.strftime('%Y-%m', Order.created_at)
    else:  # week
        time_group = func.strftime('%Y-W%W', Order.created_at)

    results = db.query(
        time_group.label('period'),
        func.sum(Order.total_amount).label('total_sales'),
        func.count(Order.id).label('order_count')
    ).filter(
        Order.status.in_(['paid', 'processing', 'shipped', 'delivered']),
        *date_filter
    ).group_by('period').order_by('period').all()

    return {
        "interval": interval,
        "data": [
            {
                "period": str(r.period),
                "total_sales": float(r.total_sales or 0),
                "order_count": r.order_count
            }
            for r in results
        ]
    }


@router.get("/top-products")
def get_top_products(
    limit: int = Query(10, ge=1, le=50),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get top-selling products by revenue or quantity
    """
    date_filter = []
    if start_date:
        date_filter.append(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        date_filter.append(Order.created_at <= datetime.fromisoformat(end_date))

    results = db.query(
        OrderItem.product_name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.subtotal).label('total_revenue')
    ).join(Order).filter(
        Order.status.in_(['paid', 'processing', 'shipped', 'delivered']),
        *date_filter
    ).group_by(OrderItem.product_name).order_by(
        func.sum(OrderItem.subtotal).desc()
    ).limit(limit).all()

    return {
        "products": [
            {
                "name": r.product_name,
                "quantity_sold": r.total_quantity,
                "revenue": float(r.total_revenue)
            }
            for r in results
        ]
    }


@router.get("/top-artists")
def get_top_artists(
    limit: int = Query(10, ge=1, le=50),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get top-performing artists by sales
    """
    date_filter = []
    if start_date:
        date_filter.append(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        date_filter.append(Order.created_at <= datetime.fromisoformat(end_date))

    results = db.query(
        Artist.name,
        Artist.id,
        func.sum(OrderItem.subtotal).label('total_revenue'),
        func.sum(OrderItem.quantity).label('total_items_sold'),
        func.avg(OrderItem.artist_commission_rate).label('avg_commission_rate')
    ).join(OrderItem, Artist.id == OrderItem.artist_id).join(
        Order
    ).filter(
        Order.status.in_(['paid', 'processing', 'shipped', 'delivered']),
        *date_filter
    ).group_by(Artist.id).order_by(
        func.sum(OrderItem.subtotal).desc()
    ).limit(limit).all()

    return {
        "artists": [
            {
                "id": r.id,
                "name": r.name,
                "revenue": float(r.total_revenue),
                "items_sold": r.total_items_sold,
                "avg_commission_rate": float(r.avg_commission_rate or 0),
                "estimated_commission": float(r.total_revenue) * float(r.avg_commission_rate or 0) / 100
            }
            for r in results
        ]
    }


@router.get("/order-status-breakdown")
def get_order_status_breakdown(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get count of orders by status (for pie chart)
    """
    date_filter = []
    if start_date:
        date_filter.append(Order.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        date_filter.append(Order.created_at <= datetime.fromisoformat(end_date))

    results = db.query(
        Order.status,
        func.count(Order.id).label('count')
    ).filter(*date_filter).group_by(Order.status).all()

    return {
        "statuses": [
            {
                "status": r.status,
                "count": r.count
            }
            for r in results
        ]
    }


@router.get("/recent-orders")
def get_recent_orders(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get recent orders for admin overview
    """
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()

    return {
        "orders": [
            {
                "id": order.id,
                "order_number": order.order_number,
                "customer_email": order.customer_email,
                "total_amount": float(order.total_amount),
                "status": order.status,
                "created_at": order.created_at.isoformat()
            }
            for order in orders
        ]
    }


@router.get("/user-growth")
def get_user_growth(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = Query("month", pattern="^(day|week|month)$"),
    db: Session = Depends(get_db)
):
    """
    Get user registration growth over time
    """
    date_filter = []
    if start_date:
        date_filter.append(User.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        date_filter.append(User.created_at <= datetime.fromisoformat(end_date))

    # Group by interval
    if interval == "day":
        time_group = func.date(User.created_at)
    elif interval == "month":
        time_group = func.strftime('%Y-%m', User.created_at)
    else:  # week
        time_group = func.strftime('%Y-W%W', User.created_at)

    results = db.query(
        time_group.label('period'),
        func.count(User.id).label('new_users')
    ).filter(*date_filter).group_by('period').order_by('period').all()

    return {
        "interval": interval,
        "data": [
            {
                "period": str(r.period),
                "new_users": r.new_users
            }
            for r in results
        ]
    }


@router.get("/low-stock-alerts")
def get_low_stock_alerts(db: Session = Depends(get_db)):
    """
    Get products with low stock (below threshold)
    """
    variants = db.query(ProductVariant).filter(
        ProductVariant.is_active == True,
        ProductVariant.track_inventory == True,
        ProductVariant.stock_quantity <= ProductVariant.low_stock_threshold
    ).all()

    return {
        "low_stock_items": [
            {
                "variant_id": v.id,
                "sku": v.sku,
                "name": v.name,
                "stock_quantity": v.stock_quantity,
                "low_stock_threshold": v.low_stock_threshold
            }
            for v in variants
        ],
        "total_count": len(variants)
    }

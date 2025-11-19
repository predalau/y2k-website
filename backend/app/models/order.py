"""
Order and OrderItem models for purchase orders
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)  # pending, paid, processing, shipped, delivered, cancelled, refunded

    # Pricing
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    shipping_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)

    # Address snapshots (FK but data should be copied at order time)
    shipping_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    billing_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)

    # Customer info snapshot
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(50), nullable=True)

    # Notes and tracking
    notes = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    tracking_number = Column(String(255), nullable=True)

    # Timestamps
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="orders")
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=True)  # For commission tracking

    # Snapshot of product data at purchase time
    product_name = Column(String(255), nullable=False)
    variant_name = Column(String(255), nullable=False)
    sku = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)  # price * quantity

    # Artist commission snapshot
    artist_commission_rate = Column(Numeric(5, 2), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    order = relationship("Order", back_populates="order_items")
    variant = relationship("ProductVariant", back_populates="order_items")
    artist = relationship("Artist")
    reviews = relationship("Review", back_populates="order_item")

"""
Inventory log model for tracking stock changes
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False, index=True)
    change_type = Column(String(50), nullable=False)  # 'sale', 'restock', 'adjustment', 'return'
    quantity_change = Column(Integer, nullable=False)  # Positive or negative
    quantity_after = Column(Integer, nullable=False)  # Stock after this change
    reference_id = Column(Integer, nullable=True)  # Order ID or other reference
    notes = Column(String(500), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Admin who made change
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    variant = relationship("ProductVariant", back_populates="inventory_logs")
    creator = relationship("User")

"""
Artist model for local artists who create merchandise designs
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    bio = Column(Text, nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    banner_image_url = Column(String(500), nullable=True)
    website = Column(String(500), nullable=True)
    instagram = Column(String(255), nullable=True)
    twitter = Column(String(255), nullable=True)
    commission_rate = Column(Numeric(5, 2), default=0.00, nullable=False)  # Percentage 0-100
    is_active = Column(Boolean, default=True, nullable=False)
    featured = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    products = relationship("Product", back_populates="artist")

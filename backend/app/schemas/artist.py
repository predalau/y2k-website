"""
Pydantic schemas for Artist API
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ArtistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    banner_image_url: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = Field(None, max_length=255)
    twitter: Optional[str] = Field(None, max_length=255)
    commission_rate: Decimal = Field(default=Decimal("0.00"), ge=0, le=100)
    is_active: bool = True
    featured: bool = False


class ArtistCreate(ArtistBase):
    """Schema for creating a new artist"""
    pass


class ArtistUpdate(BaseModel):
    """Schema for updating an artist (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    banner_image_url: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    commission_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None
    featured: Optional[bool] = None


class Artist(ArtistBase):
    """Schema for artist response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ArtistList(BaseModel):
    """Schema for artist list response"""
    id: int
    name: str
    slug: str
    profile_image_url: Optional[str]
    commission_rate: Decimal
    is_active: bool
    featured: bool

    class Config:
        from_attributes = True

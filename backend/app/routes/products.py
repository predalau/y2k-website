"""
Product API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.product import Product, ProductVariant, ProductImage
from app.schemas.product import (
    Product as ProductSchema,
    ProductCreate,
    ProductUpdate,
    ProductList,
    ProductWithDetails,
)

router = APIRouter()


@router.get("/", response_model=List[ProductList])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    featured: Optional[bool] = None,
    artist_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of products with optional filters
    """
    query = db.query(Product)

    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    if featured is not None:
        query = query.filter(Product.featured == featured)
    if artist_id is not None:
        query = query.filter(Product.artist_id == artist_id)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductWithDetails)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by ID with all details (variants, images)
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/slug/{slug}", response_model=ProductWithDetails)
def get_product_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Get a product by slug (URL-friendly identifier)
    """
    product = db.query(Product).filter(Product.slug == slug).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductSchema)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product (admin only - add auth later)
    """
    # Check if slug already exists
    existing = db.query(Product).filter(Product.slug == product.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product with this slug already exists")

    # Create product without variants and images first
    product_data = product.model_dump(exclude={'variants', 'images'})
    db_product = Product(**product_data)
    db.add(db_product)
    db.flush()  # Get the ID without committing

    # Add variants if provided
    if product.variants:
        for variant_data in product.variants:
            variant = ProductVariant(**variant_data.model_dump(), product_id=db_product.id)
            db.add(variant)

    # Add images if provided
    if product.images:
        for image_data in product.images:
            image = ProductImage(**image_data.model_dump(), product_id=db_product.id)
            db.add(image)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.patch("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a product (admin only - add auth later)
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update only provided fields
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product (soft delete by setting is_active=False)
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.is_active = False
    db.commit()
    return {"message": "Product deactivated successfully"}

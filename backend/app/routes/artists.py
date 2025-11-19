"""
Artist API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.artist import Artist
from app.schemas.artist import (
    Artist as ArtistSchema,
    ArtistCreate,
    ArtistUpdate,
    ArtistList,
)

router = APIRouter()


@router.get("/", response_model=List[ArtistList])
def get_artists(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of artists with optional filters
    """
    query = db.query(Artist)

    if is_active is not None:
        query = query.filter(Artist.is_active == is_active)
    if featured is not None:
        query = query.filter(Artist.featured == featured)

    artists = query.offset(skip).limit(limit).all()
    return artists


@router.get("/{artist_id}", response_model=ArtistSchema)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    """
    Get a single artist by ID
    """
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.get("/slug/{slug}", response_model=ArtistSchema)
def get_artist_by_slug(slug: str, db: Session = Depends(get_db)):
    """
    Get an artist by slug
    """
    artist = db.query(Artist).filter(Artist.slug == slug).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.post("/", response_model=ArtistSchema)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    """
    Create a new artist (admin only - add auth later)
    """
    # Check if slug already exists
    existing = db.query(Artist).filter(Artist.slug == artist.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Artist with this slug already exists")

    db_artist = Artist(**artist.model_dump())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


@router.patch("/{artist_id}", response_model=ArtistSchema)
def update_artist(
    artist_id: int,
    artist_update: ArtistUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an artist (admin only - add auth later)
    """
    db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not db_artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    update_data = artist_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_artist, field, value)

    db.commit()
    db.refresh(db_artist)
    return db_artist


@router.delete("/{artist_id}")
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    """
    Deactivate an artist (soft delete)
    """
    db_artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not db_artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    db_artist.is_active = False
    db.commit()
    return {"message": "Artist deactivated successfully"}

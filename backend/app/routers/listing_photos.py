from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, deps, schemas

router = APIRouter()


@router.post("/listings/{listing_id}/photos", response_model=schemas.ListingPhotoRead)
def create_listing_photo(
    *,
    db: Session = Depends(deps.get_db),
    listing_id: int,
    photo: schemas.ListingPhotoCreate,
):
    # Verify listing exists
    listing = crud.get_listing(db=db, listing_id=listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Check photo limit (max 10)
    photo_count = crud.count_listing_photos(db=db, listing_id=listing_id)
    if photo_count >= 10:
        raise HTTPException(status_code=400, detail="Maximum 10 photos per listing")
    
    # Ensure listing_id matches
    photo.listing_id = listing_id
    return crud.create_listing_photo(db=db, photo=photo)


@router.get("/listings/{listing_id}/photos", response_model=list[schemas.ListingPhotoRead])
def read_listing_photos(
    *,
    db: Session = Depends(deps.get_db),
    listing_id: int,
):
    # Verify listing exists
    listing = crud.get_listing(db=db, listing_id=listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    return crud.get_listing_photos(db=db, listing_id=listing_id)


@router.delete("/photos/{photo_id}")
def delete_listing_photo(
    *,
    db: Session = Depends(deps.get_db),
    photo_id: int,
):
    if not crud.delete_listing_photo(db=db, photo_id=photo_id):
        raise HTTPException(status_code=404, detail="Photo not found")
    return {"ok": True}

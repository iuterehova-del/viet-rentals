from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, deps, schemas

router = APIRouter()


@router.post("/", response_model=schemas.ListingRead)
def create_listing(*, db: Session = Depends(deps.get_db), listing: schemas.ListingCreate):
    return crud.create_listing(db=db, listing=listing)


@router.get("/", response_model=list[schemas.ListingRead])
def read_listings(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    return crud.get_listings(db=db, skip=skip, limit=limit)


@router.get("/public", response_model=list[schemas.ListingRead])
def read_public_listings(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    return crud.get_public_listings(db=db, skip=skip, limit=limit)


@router.get("/{listing_id}", response_model=schemas.ListingRead)
def read_listing(*, db: Session = Depends(deps.get_db), listing_id: int):
    db_obj = crud.get_listing(db=db, listing_id=listing_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Listing not found")
    return db_obj


@router.put("/{listing_id}", response_model=schemas.ListingRead)
def update_listing(*, db: Session = Depends(deps.get_db), listing_id: int, listing: schemas.ListingUpdate):
    db_obj = crud.update_listing(db=db, listing_id=listing_id, listing=listing)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Listing not found")
    return db_obj


@router.delete("/{listing_id}")
def delete_listing(*, db: Session = Depends(deps.get_db), listing_id: int):
    if not crud.delete_listing(db=db, listing_id=listing_id):
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"ok": True}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, deps, schemas

router = APIRouter()


@router.post("/", response_model=schemas.RealtorRead)
def create_realtor(*, db: Session = Depends(deps.get_db), realtor: schemas.RealtorCreate):
    return crud.create_realtor(db=db, realtor=realtor)


@router.get("/", response_model=list[schemas.RealtorRead])
def read_realtors(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    return crud.get_realtors(db=db, skip=skip, limit=limit)


@router.get("/{realtor_id}", response_model=schemas.RealtorRead)
def read_realtor(*, db: Session = Depends(deps.get_db), realtor_id: int):
    db_obj = crud.get_realtor(db=db, realtor_id=realtor_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Realtor not found")
    return db_obj


@router.put("/{realtor_id}", response_model=schemas.RealtorRead)
def update_realtor(*, db: Session = Depends(deps.get_db), realtor_id: int, realtor: schemas.RealtorUpdate):
    db_obj = crud.update_realtor(db=db, realtor_id=realtor_id, realtor=realtor)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Realtor not found")
    return db_obj


@router.delete("/{realtor_id}")
def delete_realtor(*, db: Session = Depends(deps.get_db), realtor_id: int):
    if not crud.delete_realtor(db=db, realtor_id=realtor_id):
        raise HTTPException(status_code=404, detail="Realtor not found")
    return {"ok": True}

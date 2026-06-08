from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import crud, deps, schemas

router = APIRouter()


@router.post("/", response_model=schemas.PaymentRead)
def create_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment: schemas.PaymentCreate,
):
    # Verify realtor exists
    realtor = crud.get_realtor(db=db, realtor_id=payment.realtor_id)
    if not realtor:
        raise HTTPException(status_code=404, detail="Realtor not found")
    
    return crud.create_payment(db=db, payment=payment)


@router.get("/", response_model=list[schemas.PaymentRead])
def read_payments(
    *,
    db: Session = Depends(deps.get_db),
    realtor_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    if realtor_id:
        return crud.get_payments_by_realtor(db=db, realtor_id=realtor_id, skip=skip, limit=limit)
    return crud.get_payments(db=db, skip=skip, limit=limit)


@router.get("/{payment_id}", response_model=schemas.PaymentRead)
def read_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment_id: int,
):
    db_obj = crud.get_payment(db=db, payment_id=payment_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_obj


@router.put("/{payment_id}", response_model=schemas.PaymentRead)
def update_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment_id: int,
    payment: schemas.PaymentUpdate,
):
    db_obj = crud.update_payment(db=db, payment_id=payment_id, payment=payment)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_obj


@router.delete("/{payment_id}")
def delete_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment_id: int,
):
    if not crud.delete_payment(db=db, payment_id=payment_id):
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"ok": True}

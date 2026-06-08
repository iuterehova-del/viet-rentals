from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, deps, schemas

router = APIRouter()


@router.post("/", response_model=schemas.SubscriptionRead)
def create_subscription(*, db: Session = Depends(deps.get_db), subscription: schemas.SubscriptionCreate):
    return crud.create_subscription(db=db, subscription=subscription)


@router.get("/", response_model=list[schemas.SubscriptionRead])
def read_subscriptions(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    return crud.get_subscriptions(db=db, skip=skip, limit=limit)


@router.get("/{subscription_id}", response_model=schemas.SubscriptionRead)
def read_subscription(*, db: Session = Depends(deps.get_db), subscription_id: int):
    db_obj = crud.get_subscription(db=db, subscription_id=subscription_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_obj


@router.put("/{subscription_id}", response_model=schemas.SubscriptionRead)
def update_subscription(*, db: Session = Depends(deps.get_db), subscription_id: int, subscription: schemas.SubscriptionUpdate):
    db_obj = crud.update_subscription(db=db, subscription_id=subscription_id, subscription=subscription)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_obj


@router.delete("/{subscription_id}")
def delete_subscription(*, db: Session = Depends(deps.get_db), subscription_id: int):
    if not crud.delete_subscription(db=db, subscription_id=subscription_id):
        raise HTTPException(status_code=404, detail="Subscription not found")
    return {"ok": True}

from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from . import models, schemas


# Realtors

def get_realtor(db: Session, realtor_id: int) -> Optional[models.Realtor]:
    return db.query(models.Realtor).filter(models.Realtor.id == realtor_id).first()


def get_realtors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Realtor]:
    return db.query(models.Realtor).offset(skip).limit(limit).all()


def create_realtor(db: Session, realtor: schemas.RealtorCreate) -> models.Realtor:
    db_obj = models.Realtor(**realtor.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_realtor(db: Session, realtor_id: int, realtor: schemas.RealtorUpdate) -> Optional[models.Realtor]:
    db_obj = get_realtor(db, realtor_id)
    if not db_obj:
        return None
    for key, value in realtor.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_realtor(db: Session, realtor_id: int) -> bool:
    db_obj = get_realtor(db, realtor_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


# Subscriptions

def get_subscription(db: Session, subscription_id: int) -> Optional[models.Subscription]:
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()


def get_subscriptions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Subscription]:
    return db.query(models.Subscription).offset(skip).limit(limit).all()


def create_subscription(db: Session, subscription: schemas.SubscriptionCreate) -> models.Subscription:
    db_obj = models.Subscription(**subscription.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_subscription(db: Session, subscription_id: int, subscription: schemas.SubscriptionUpdate) -> Optional[models.Subscription]:
    db_obj = get_subscription(db, subscription_id)
    if not db_obj:
        return None
    for key, value in subscription.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_subscription(db: Session, subscription_id: int) -> bool:
    db_obj = get_subscription(db, subscription_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


def get_active_subscription_by_realtor(db: Session, realtor_id: int) -> Optional[models.Subscription]:
    now = datetime.utcnow()
    return (
        db.query(models.Subscription)
        .filter(
            models.Subscription.realtor_id == realtor_id,
            models.Subscription.is_active == True,
            models.Subscription.ends_at > now,
        )
        .order_by(models.Subscription.ends_at.desc())
        .first()
    )


# Listings

def get_listing(db: Session, listing_id: int) -> Optional[models.Listing]:
    return db.query(models.Listing).filter(models.Listing.id == listing_id).first()


def get_listings(db: Session, skip: int = 0, limit: int = 100) -> List[models.Listing]:
    return db.query(models.Listing).offset(skip).limit(limit).all()


def create_listing(db: Session, listing: schemas.ListingCreate) -> models.Listing:
    db_obj = models.Listing(**listing.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_listing(db: Session, listing_id: int, listing: schemas.ListingUpdate) -> Optional[models.Listing]:
    db_obj = get_listing(db, listing_id)
    if not db_obj:
        return None
    for key, value in listing.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_listing(db: Session, listing_id: int) -> bool:
    db_obj = get_listing(db, listing_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


def get_public_listings(db: Session, skip: int = 0, limit: int = 100) -> List[models.Listing]:
    now = datetime.utcnow()
    return (
        db.query(models.Listing)
        .join(models.Realtor)
        .join(models.Subscription, models.Subscription.realtor_id == models.Realtor.id)
        .filter(
            models.Listing.is_published == True,
            models.Subscription.is_active == True,
            models.Subscription.ends_at > now,
        )
        .order_by(models.Listing.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

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


# Listing Photos

def get_listing_photos(db: Session, listing_id: int) -> List[models.ListingPhoto]:
    return (
        db.query(models.ListingPhoto)
        .filter(models.ListingPhoto.listing_id == listing_id)
        .order_by(models.ListingPhoto.sort_order)
        .all()
    )


def count_listing_photos(db: Session, listing_id: int) -> int:
    return db.query(models.ListingPhoto).filter(models.ListingPhoto.listing_id == listing_id).count()


def create_listing_photo(db: Session, photo: schemas.ListingPhotoCreate) -> models.ListingPhoto:
    db_obj = models.ListingPhoto(**photo.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_listing_photo(db: Session, photo_id: int) -> Optional[models.ListingPhoto]:
    return db.query(models.ListingPhoto).filter(models.ListingPhoto.id == photo_id).first()


def delete_listing_photo(db: Session, photo_id: int) -> bool:
    db_obj = get_listing_photo(db, photo_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True


# Payments

def get_payment(db: Session, payment_id: int) -> Optional[models.Payment]:
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()


def get_payments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Payment]:
    return db.query(models.Payment).offset(skip).limit(limit).all()


def get_payments_by_realtor(db: Session, realtor_id: int, skip: int = 0, limit: int = 100) -> List[models.Payment]:
    return (
        db.query(models.Payment)
        .filter(models.Payment.realtor_id == realtor_id)
        .order_by(models.Payment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_payment(db: Session, payment: schemas.PaymentCreate) -> models.Payment:
    db_obj = models.Payment(**payment.dict())
    db.add(db_obj)
    db.flush()
    
    # If payment is marked as "paid", extend subscription
    if payment.status == "paid":
        extend_realtor_subscription(db, payment.realtor_id, payment.period_end)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj


def extend_realtor_subscription(db: Session, realtor_id: int, new_end_date: datetime) -> bool:
    """Extend or create subscription for realtor after successful payment."""
    active_sub = get_active_subscription_by_realtor(db, realtor_id)
    
    if active_sub:
        # Extend existing subscription
        active_sub.ends_at = new_end_date
        active_sub.is_active = True
    else:
        # Create new subscription (use period_start from payment as starts_at)
        # This assumes payment.period_start is passed; adjust as needed
        new_sub = models.Subscription(
            realtor_id=realtor_id,
            plan_name="Standard",
            price=0,  # Price should come from payment
            starts_at=datetime.utcnow(),
            ends_at=new_end_date,
            is_active=True,
        )
        db.add(new_sub)
    
    db.commit()
    return True


def update_payment(db: Session, payment_id: int, payment: schemas.PaymentUpdate) -> Optional[models.Payment]:
    db_obj = get_payment(db, payment_id)
    if not db_obj:
        return None
    
    # If status is being changed to "paid", trigger subscription extension
    if payment.status == "paid" and db_obj.status != "paid":
        extend_realtor_subscription(db, db_obj.realtor_id, db_obj.period_end)
    
    for key, value in payment.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_payment(db: Session, payment_id: int) -> bool:
    db_obj = get_payment(db, payment_id)
    if not db_obj:
        return False
    db.delete(db_obj)
    db.commit()
    return True

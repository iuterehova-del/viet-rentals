from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Realtor(Base):
    __tablename__ = "realtors"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(50), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    subscriptions = relationship(
        "Subscription", back_populates="realtor", cascade="all, delete-orphan"
    )
    listings = relationship("Listing", back_populates="realtor", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="realtor", cascade="all, delete-orphan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    realtor_id = Column(Integer, ForeignKey("realtors.id", ondelete="CASCADE"), nullable=False)
    plan_name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    realtor = relationship("Realtor", back_populates="subscriptions")


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    realtor_id = Column(Integer, ForeignKey("realtors.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(12, 2), nullable=False)
    address = Column(String(255), nullable=True)
    city = Column(String(120), nullable=False, default="Nha Trang")
    is_published = Column(Boolean, nullable=False, default=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    realtor = relationship("Realtor", back_populates="listings")
    photos = relationship("ListingPhoto", back_populates="listing", cascade="all, delete-orphan")


class ListingPhoto(Base):
    __tablename__ = "listing_photos"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    cloudinary_public_id = Column(String(255), nullable=False)
    url = Column(String(1024), nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    listing = relationship("Listing", back_populates="photos")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    realtor_id = Column(Integer, ForeignKey("realtors.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    realtor = relationship("Realtor", back_populates="payments")

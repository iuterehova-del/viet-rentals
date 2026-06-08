from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class RealtorBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: Optional[bool] = True


class RealtorCreate(RealtorBase):
    pass


class RealtorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class RealtorRead(RealtorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SubscriptionBase(BaseModel):
    plan_name: str
    price: float
    starts_at: datetime
    ends_at: datetime
    is_active: Optional[bool] = True


class SubscriptionCreate(SubscriptionBase):
    realtor_id: int


class SubscriptionUpdate(BaseModel):
    plan_name: Optional[str] = None
    price: Optional[float] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    is_active: Optional[bool] = None


class SubscriptionRead(SubscriptionBase):
    id: int
    realtor_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    address: Optional[str] = None
    city: Optional[str] = "Nha Trang"
    is_published: Optional[bool] = True
    published_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class ListingCreate(ListingBase):
    realtor_id: int


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    is_published: Optional[bool] = None
    published_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class ListingRead(ListingBase):
    id: int
    realtor_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    amount: float
    currency: str
    paid_at: datetime
    period_start: datetime
    period_end: datetime
    status: str


class PaymentCreate(PaymentBase):
    realtor_id: int


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    paid_at: Optional[datetime] = None
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    status: Optional[str] = None


class PaymentRead(PaymentBase):
    id: int
    realtor_id: int
    created_at: datetime

    class Config:
        orm_mode = True

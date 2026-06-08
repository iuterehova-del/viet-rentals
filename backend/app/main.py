from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import engine
from .models import Base
from .routers import listings, listing_photos, payments, realtors, subscriptions


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (if needed)


app = FastAPI(title="Viet Rentals API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(realtors.router, prefix="/realtors", tags=["realtors"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(listings.router, prefix="/listings", tags=["listings"])
app.include_router(listing_photos.router, tags=["listing_photos"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])

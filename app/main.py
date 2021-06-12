from typing import List

from fastapi import Depends, FastAPI

from . import models
from .database import SessionLocal, engine
from .routers import companies

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ICE API",
    description="ICE BackEnd REST API",
    version="1.0",)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(
    companies.router,
    prefix="/api/v1",
    tags=["Companies Endpoints"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

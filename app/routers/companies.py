from app import companies_crud
from typing import List

from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session

from .. import schemas, companies_crud
from ..database import SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/companies/", response_model=schemas.Company)
async def create_article(company: schemas.Company, db: Session = Depends(get_db)):
    db_company = companies_crud.get_company(db, company.vat_number)
    if db_company:
        raise HTTPException(status_code=400, detail="Company already registered")
    return companies_crud.create_company(db, company)
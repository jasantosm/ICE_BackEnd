from app import companies_crud
from typing import Dict, List

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
async def create_company(company: schemas.Company, db: Session = Depends(get_db)):
    db_company = companies_crud.get_company(db, company.vat_number)
    if db_company:
        raise HTTPException(status_code=400, detail="Company already registered")
    return companies_crud.create_company(db, company)

@router.get("/companies/{vat_number}", response_model=schemas.Company)
async def get_company(vat_number: int, db: Session = Depends(get_db)):
    db_company = companies_crud.get_company(db, vat_number)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not registered")
    return db_company

@router.get("/companies/all/{limit}", response_model=List[schemas.Company])
async def get_companies(limit: int, db: Session = Depends(get_db)):
    return companies_crud.get_companies(db, limit)

@router.delete("/companies/{vat_number}", response_model=schemas.Company)
async def delete_company(vat_number: int, db: Session = Depends(get_db)):
    db_company = companies_crud.get_company(db, vat_number)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not registered")
    return companies_crud.delete_company(db, vat_number)

@router.put("/companies/{vat_number}", response_model=schemas.Company)
async def update_company(vat_number: int, update_fields: Dict, db: Session = Depends(get_db)):
    db_company = companies_crud.get_company(db, vat_number)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not registered")
    return companies_crud.update_company(db, vat_number, update_fields)
from app import companies_crud
from typing import Dict, List

from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, companies_crud, users_crud
from ..database import SessionLocal
from ..auth import AuthHandler

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
auth_handler = AuthHandler()

@router.post("/companies/", response_model=schemas.Company, status_code=status.HTTP_201_CREATED)
async def create_company(company: schemas.Company, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:
        db_company = companies_crud.get_company(db, company.vat_number)
        if db_company:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company already registered")
        return companies_crud.create_company(db, company)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.get("/companies/{vat_number}", response_model=schemas.Company, status_code=status.HTTP_200_OK)
async def get_company(vat_number: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:
        db_company = companies_crud.get_company(db, vat_number)
        if not db_company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not registered")
        return db_company
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.get("/companies/all/{limit}", response_model=List[schemas.Company], status_code=status.HTTP_200_OK)
async def get_companies(limit: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:
        return companies_crud.get_companies(db, limit)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.delete("/companies/{vat_number}", response_model=schemas.Company, status_code=status.HTTP_200_OK)
async def delete_company(vat_number: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:
        db_company = companies_crud.get_company(db, vat_number)
        if not db_company:
            raise HTTPException(status_code=404, detail="Company not registered")
        return companies_crud.delete_company(db, vat_number)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.put("/companies/{vat_number}", response_model=schemas.Company, status_code=status.HTTP_202_ACCEPTED)
async def update_company(vat_number: int, update_fields: Dict, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:    
        db_company = companies_crud.get_company(db, vat_number)
        if not db_company:
            raise HTTPException(status_code=404, detail="Company not registered")
        return companies_crud.update_company(db, vat_number, update_fields)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")
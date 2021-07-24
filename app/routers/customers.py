from app import customers_crud
from typing import Dict, List

from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, customers_crud, users_crud
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

@router.post("/customers/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: schemas.Customer, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin:
        db_customer = customers_crud.get_customer(db, customer.vat_number)
        if db_customer:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer already registered")
        return customers_crud.create_customer(db, customer)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.get("/customers/{vat_number}", response_model=schemas.Customer, status_code=status.HTTP_200_OK)
async def get_customer(vat_number: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin or db_user.is_customer:
        db_customer = customers_crud.get_customer(db, vat_number)
        if not db_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not registered")
        return db_customer
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.get("/customers/all/{limit}", response_model=List[schemas.Customer], status_code=status.HTTP_200_OK)
async def get_companies(limit: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin or db_user.is_customer:
        return customers_crud.get_customers(db, limit)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.delete("/customers/{vat_number}", response_model=schemas.Customer, status_code=status.HTTP_200_OK)
async def delete_customer(vat_number: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin:
        db_customer = customers_crud.get_customer(db, vat_number)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not registered")
        return customers_crud.delete_customer(db, vat_number)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.put("/customers/{vat_number}", response_model=schemas.Customer, status_code=status.HTTP_202_ACCEPTED)
async def update_customer(vat_number: int, update_fields: Dict, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin:    
        db_customer = customers_crud.get_customer(db, vat_number)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not registered")
        return customers_crud.update_customer(db, vat_number, update_fields)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")
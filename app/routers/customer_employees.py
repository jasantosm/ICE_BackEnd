from typing import Dict, List

from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, customer_employees_crud, users_crud
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

@router.post("/customeremployees/", response_model=schemas.CustomerEmployee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: schemas.CustomerEmployee, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin:
        db_employee = customer_employees_crud.get_employee(db, employee.user_id)
        if db_employee:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee already registered")
        return customer_employees_crud.create_employee(db, employee)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")


@router.get("/customeremployees/{user_id}", response_model=schemas.CustomerEmployee, status_code=status.HTTP_200_OK)
async def get_employee(user_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin or db_user.is_customer:
        db_employee = customer_employees_crud.get_employee(db, user_id)
        if not db_employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not registered")
        return db_employee
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")


@router.get("/customeremployees/all/{limit}", response_model=List[schemas.CustomerEmployee], status_code=status.HTTP_200_OK)
async def get_employees(limit: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin or db_user.is_customer:
        return customer_employees_crud.get_employees(db, limit)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")


@router.delete("/customeremployees/{user_id}", response_model=schemas.CustomerEmployee, status_code=status.HTTP_200_OK)
async def delete_employee(user_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin:
        db_employee = customer_employees_crud.get_employee(db, user_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not registered")
        return customer_employees_crud.delete_employee(db, user_id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.put("/customeremployees/{user_id}", response_model=schemas.CustomerEmployee, status_code=status.HTTP_202_ACCEPTED)
async def update_employee(user_id: int, update_fields: Dict, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super or db_user.is_admin:    
        db_employee = customer_employees_crud.get_employee(db, user_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not registered")
        return customer_employees_crud.update_employee(db, user_id, update_fields)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")
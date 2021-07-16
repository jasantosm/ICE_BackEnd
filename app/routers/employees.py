from app import companies_crud
from typing import Dict, List

from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, employees_crud, users_crud
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

@router.post("/employees/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: schemas.Employee, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_employee = employees_crud.get_employee(db, employee.user_id)
        if db_employee:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee already registered")
        return employees_crud.create_employee(db, employee)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")


@router.get("/employees/{user_id}", response_model=schemas.Employee, status_code=status.HTTP_200_OK)
async def get_employee(user_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:
        db_employee = employees_crud.get_employee(db, user_id)
        if not db_employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not registered")
        return db_employee
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")


@router.get("/employees/all/{limit}", response_model=List[schemas.Employee], status_code=status.HTTP_200_OK)
async def get_employees(limit: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:
        return employees_crud.get_employees(db, limit)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.delete("/employees/{user_id}", response_model=schemas.Employee, status_code=status.HTTP_200_OK)
async def delete_employee(user_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:
        db_employee = employees_crud.get_employee(db, user_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not registered")
        return employees_crud.delete_employee(db, user_id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.put("/employees/{user_id}", response_model=schemas.Employee, status_code=status.HTTP_202_ACCEPTED)
async def update_company(user_id: int, update_fields: Dict, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:    
        db_employee = employees_crud.get_employee(db, user_id)
        if not db_employee:
            raise HTTPException(status_code=404, detail="Employee not registered")
        return employees_crud.update_employee(db, user_id, update_fields)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")
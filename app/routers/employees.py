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

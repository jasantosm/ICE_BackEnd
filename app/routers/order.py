from typing import Dict, List

from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, orders_crud, users_crud
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

@router.post("/orders/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.Order, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_order = orders_crud.get_order(db, order.id)
        if db_order:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order already registered")
        return orders_crud.create_order(db, order)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")


@router.get("/orders/{order_id}", response_model=schemas.Order, status_code=status.HTTP_200_OK)
async def get_order(order_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_order = orders_crud.get_order(db, order_id)
        if not db_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not registered")
        return db_order
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.get("/orders/all/{limit}", response_model=List[schemas.Order], status_code=status.HTTP_200_OK)
async def get_orders(limit: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        return orders_crud.get_orders(db, limit)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.delete("/orders/{order_id}", response_model=schemas.Order, status_code=status.HTTP_200_OK)
async def delete_order(order_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_order = orders_crud.get_order(db, order_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not registered")
        return orders_crud.delete_order(db, order_id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.put("/orders/{user_id}", response_model=schemas.Order, status_code=status.HTTP_202_ACCEPTED)
async def update_order(user_id: int, update_fields: Dict, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:   
        db_order = orders_crud.get_order(db, user_id)
        if not db_order:
            raise HTTPException(status_code=404, detail="Order not registered")
        return orders_crud.update_order(db, user_id, update_fields)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")
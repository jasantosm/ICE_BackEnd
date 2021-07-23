from typing import Dict, List

from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, forwarders_crud, users_crud
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

@router.post("/forwarders/", response_model=schemas.Forwarder, status_code=status.HTTP_201_CREATED)
async def create_forwarder(forwarder: schemas.Forwarder, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_forwarder = forwarders_crud.get_forwarder(db, forwarder.id)
        if db_forwarder:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Forwarder already registered")
        return forwarders_crud.create_forwarder(db, forwarder)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.get("/forwarders/{forwarder_id}", response_model=schemas.Forwarder, status_code=status.HTTP_200_OK)
async def get_forwarder(forwarder_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_forwarder = forwarders_crud.get_forwarder(db, forwarder_id)
        if not db_forwarder:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forwarder not registered")
        return db_forwarder
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.get("/forwarders/all/", response_model=List[schemas.Forwarder], status_code=status.HTTP_200_OK)
async def get_forwarders(db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        return forwarders_crud.get_forwarders(db)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.delete("/forwarders/{forwarder_id}", response_model=schemas.Forwarder, status_code=status.HTTP_200_OK)
async def delete_forwarder(forwarder_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:
        db_forwarder = forwarders_crud.get_forwarder(db, forwarder_id)
        if not db_forwarder:
            raise HTTPException(status_code=404, detail="Forwarder not registered")
        return forwarders_crud.delete_forwarder(db, forwarder_id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.put("/forwarders/{forwarder_id}", response_model=schemas.Forwarder, status_code=status.HTTP_202_ACCEPTED)
async def update_forwarder(user_id: int, update_fields: Dict, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin:    
        db_forwarder = forwarders_crud.get_forwarder(db, user_id)
        if not db_forwarder:
            raise HTTPException(status_code=404, detail="Forwarder not registered")
        return forwarders_crud.update_forwarder(db, user_id, update_fields)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")
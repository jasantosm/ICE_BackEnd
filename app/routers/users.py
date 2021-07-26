from typing import Dict, List

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from .. import schemas, users_crud
from ..auth import AuthHandler
from ..database import SessionLocal


ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

auth_handler = AuthHandler()


@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.User, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):  
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_user = users_crud.get_user(db, user.email)
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
        user.password = auth_handler.get_password_hash(user.password)
        
        return users_crud.create_user(db, user)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")


@router.post("/token/", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_handler.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_handler.create_token(user, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_user = users_crud.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not registered")
        return db_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.get("/users/all/{limit}", response_model=List[schemas.User], status_code=status.HTTP_200_OK)
async def get_users(limit: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        return users_crud.get_users(db, limit)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")


@router.delete("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:
        db_user = users_crud.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not registered")
        return users_crud.delete_user(db, user_id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")

@router.put("/users/{user_id}", response_model=schemas.User, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, update_fields: Dict, db: Session = Depends(get_db), useremail=Depends(auth_handler.auth_wrapper)):
    db_user = users_crud.get_user(db,useremail)
    if db_user.is_ICE_admin or db_user.is_super:   
        db_user = users_crud.get_user_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not registered")
        return users_crud.update_user(db, user_id, update_fields)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized for this method")






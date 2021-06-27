from typing import Dict, List

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from .. import schemas, users_crud
from ..auth import AuthHandler
from ..database import SessionLocal


ACCESS_TOKEN_EXPIRE_MINUTES = 5

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
async def create_user(user: schemas.User, db: Session = Depends(get_db)):  
    db_user = users_crud.get_user(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")
    user.password = auth_handler.get_password_hash(user.password)
    
    return users_crud.create_user(db, user)

@router.post("/login/", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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






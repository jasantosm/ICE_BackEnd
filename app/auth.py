from fastapi import security
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional

from . import schemas, users_crud


class AuthHandler():
    security = OAuth2PasswordBearer(tokenUrl="/api/token")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, db: Session, useremail: str, password: str):
        user = users_crud.get_user(db, useremail)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create_token(self, user: schemas.User, expires_delta):
        payload = {
            'exp': datetime.utcnow() + expires_delta,
            'iat': datetime.utcnow(),
            'sub': user.email,
            'is_super': user.is_super,
            'is_admin': user.is_admin,
            'is_customer': user.is_customer,
            'is_ICE_admin': user.is_ICE_admin
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        expired_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Signature has expired', 
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            
            useremail: str = payload.get("sub")
            if useremail is None:
                raise credentials_exception
            return useremail
        except jwt.ExpiredSignatureError:
            raise expired_exception
        except jwt.InvalidTokenError as e:
            raise credentials_exception

    def auth_wrapper(self, token: str = Depends(security)):
        return self.decode_token(token)

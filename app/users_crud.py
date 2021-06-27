from sqlalchemy.orm import Session

from fastapi import HTTPException

from . import models, schemas

def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        email = user.email,
        password = user.password,
        is_super = user.is_super,
        is_admin = user.is_admin,
        is_customer = user.is_customer
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email==email).first()
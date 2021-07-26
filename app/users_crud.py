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

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id==user_id).first()

def get_users(db: Session, limit: int):
    return db.query(models.User).limit(limit).all()

def delete_user(db: Session, user_id: int):
    obj = db.query(models.User).filter(models.User.id==user_id).first()
    db.delete(obj)
    db.commit()
    return obj

def update_user(db: Session, user_id: int, update_fields: schemas.User):

    if "id" in update_fields:
        raise HTTPException(status_code=409, detail="id field cannot be updated")
        
    db.query(models.User).filter(models.User.id==user_id).update(update_fields)
    db.commit()
    return get_user_by_id(db, user_id)
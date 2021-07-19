from sqlalchemy.orm import Session

from fastapi import HTTPException

from . import models, schemas

def create_employee(db: Session, employee: schemas.CustomerEmployee):
    db_employee = models.CustomerEmployee(
        name = employee.name,
        phone = employee.phone,
        whatsapp = employee.whatsapp,
        photo = employee.photo,
        job_title = employee.job_title,
        customer_id = employee.customer_id,
        user_id = employee.user_id
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee

def get_employee(db: Session, user_id: int):
    return db.query(models.CustomerEmployee).filter(models.CustomerEmployee.user_id==user_id).first()

def get_employees(db: Session, limit: int):
    return db.query(models.CustomerEmployee).limit(limit).all()

def delete_employee(db: Session, user_id: int):
    obj = db.query(models.CustomerEmployee).filter(models.CustomerEmployee.user_id==user_id).first()
    db.delete(obj)
    db.commit()
    return obj

def update_employee(db: Session, user_id: int, update_fields: schemas.CustomerEmployee):

    if "id" in update_fields:
        raise HTTPException(status_code=409, detail="id field cannot be updated")

    if "user_id" in update_fields:
        raise HTTPException(status_code=409, detail="user_id field cannot be updated")
        
    db.query(models.CustomerEmployee).filter(models.CustomerEmployee.user_id==user_id).update(update_fields)
    db.commit()
    return get_employee(db, user_id)
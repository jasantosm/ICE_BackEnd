from sqlalchemy.orm import Session

from fastapi import HTTPException

from . import models, schemas

def create_customer(db: Session, customer: schemas.Customer):
    db_customer = models.Customer(
        name = customer.name,
        email = customer.email,
        address = customer.address,
        city = customer.city,
        state = customer.state,
        phone = customer.phone,
        logo = customer.logo,
        vat_number = customer.vat_number,
        technical_advisor_id = customer.technical_advisor_id,
        sales_advisor_id = customer.sales_advisor_id
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer

def get_customer(db: Session, vat_number: int):
    return db.query(models.Customer).filter(models.Customer.vat_number==vat_number).first()

def get_customers(db: Session, limit: int):
    return db.query(models.Customer).limit(limit).all()

def delete_customer(db: Session, vat_number: int):
    obj = db.query(models.Customer).filter(models.Customer.vat_number==vat_number).first()
    db.delete(obj)
    db.commit()
    return obj

def update_customer(db: Session, vat_number: int, update_fields: schemas.Customer):

    if "id" in update_fields:
        raise HTTPException(status_code=409, detail="id field cannot be updated")

    if "vat_number" in update_fields:
        raise HTTPException(status_code=409, detail="vat_number field cannot be updated")
        
    db.query(models.Customer).filter(models.Customer.vat_number==vat_number).update(update_fields)
    db.commit()
    return get_customer(db, vat_number)
    


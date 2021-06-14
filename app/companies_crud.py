from sqlalchemy.orm import Session

from fastapi import HTTPException

from . import models, schemas

def create_company(db: Session, company: schemas.Company):
    db_company = models.Company(
        name = company.name,
        email = company.email,
        address = company.address,
        city = company.city,
        state = company.state,
        phone = company.phone,
        logo = company.logo,
        vat_number = company.vat_number
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company

def get_company(db: Session, vat_number: int):
    return db.query(models.Company).filter(models.Company.vat_number==vat_number).first()

def get_companies(db: Session, limit: int):
    return db.query(models.Company).limit(limit).all()

def delete_company(db: Session, vat_number: int):
    obj = db.query(models.Company).filter(models.Company.vat_number==vat_number).first()
    db.delete(obj)
    db.commit()
    return obj

def update_company(db: Session, vat_number: int, update_fields: schemas.Company):

    if "id" in update_fields:
        raise HTTPException(status_code=409, detail="id field cannot be updated")

    if "vat_number" in update_fields:
        raise HTTPException(status_code=409, detail="vat_number field cannot be updated")
        
    db.query(models.Company).filter(models.Company.vat_number==vat_number).update(update_fields)
    db.commit()
    return get_company(db, vat_number)
    


from sqlalchemy.orm import Session

from fastapi import HTTPException

from . import models, schemas

def create_forwarder(db: Session, forwarder: schemas.Forwarder):
    db_forwarder = models.Forwarder(
        name = forwarder.name,
        phone = forwarder.phone,
        extension = forwarder.extension,
        contact_person_name = forwarder.contact_person_name,
        cell_phone = forwarder.cell_phone,
        website = forwarder.website
    )

    db.add(db_forwarder)
    db.commit()
    db.refresh(db_forwarder)

    return db_forwarder

def get_forwarder(db: Session, forwarder_id: int):
    return db.query(models.Forwarder).filter(models.Forwarder.id==forwarder_id).first()

def get_forwarders(db: Session):
    return db.query(models.Forwarder).all()

def delete_forwarder(db: Session, user_id: int):
    obj = db.query(models.Forwarder).filter(models.Forwarder.id==user_id).first()
    db.delete(obj)
    db.commit()
    return obj

def update_forwarder(db: Session, forwarder_id: int, update_fields: schemas.Forwarder):

    if "id" in update_fields:
        raise HTTPException(status_code=409, detail="id field cannot be updated")
        
    db.query(models.Forwarder).filter(models.Forwarder.id==forwarder_id).update(update_fields)
    db.commit()
    return get_forwarder(db, forwarder_id)
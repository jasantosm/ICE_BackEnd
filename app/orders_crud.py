from sqlalchemy.orm import Session

from fastapi import HTTPException

from . import models, schemas

def create_order(db: Session, order: schemas.Order):
    db_order = models.Order(
        customer_number = order.customer_number,
        description = order.description,
        order_date = order.order_date,
        ETA = order.ETA,
        amount = order.amount,
        terms = order.terms,
        forwarder_id = order.forwarder_id,
        tracking_code = order.tracking_code,
        from_lat = order.from_lat,
        from_long = order.from_long,
        to_lat = order.to_lat,
        to_long = order.to_long,
        customer_id = order.customer_id,
        documents = order.documents
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id==order_id).first()

def get_orders(db: Session, limit: int):
    return db.query(models.Order).limit(limit).all()

def delete_order(db: Session, user_id: int):
    obj = db.query(models.Order).filter(models.Order.id==user_id).first()
    db.delete(obj)
    db.commit()
    return obj

def update_order(db: Session, order_id: int, update_fields: schemas.Order):

    if "id" in update_fields:
        raise HTTPException(status_code=409, detail="id field cannot be updated")
        
    db.query(models.Order).filter(models.Order.id==order_id).update(update_fields)
    db.commit()
    return get_order(db, order_id)
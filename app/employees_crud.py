from sqlalchemy.orm import Session


from . import models, schemas

def create_employee(db: Session, employee: schemas.Employee):
    db_employee = models.Employee(
        name = employee.name,
        phone = employee.phone,
        whatsapp = employee.whatsapp,
        photo = employee.photo,
        profession = employee.profession,
        job_title = employee.job_title,
        about = employee.about,
        company_id = employee.company_id,
        user_id = employee.user_id
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee

def get_employee(db: Session, user_id: int):
    return db.query(models.Employee).filter(models.Employee.user_id==user_id).first()
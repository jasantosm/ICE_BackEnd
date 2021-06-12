from pydantic.errors import EmailError
from sqlalchemy.orm import Session

from . import models, schemas

def create_company(db: Session, company: schemas.Company):
    db_company = models.Company(
        name = company.name,
        email = company.email,
        password = company.password,
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
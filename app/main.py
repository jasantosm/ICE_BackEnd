from app.routers import employees, order, users, companies, customers, customer_employees, forwarders
from typing import List

from fastapi import Depends, FastAPI

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ICE API",
    description="ICE BackEnd REST API",
    version="1.0",
    debug=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
prefix = "/api"
app.include_router(
    companies.router,
    prefix=prefix,
    tags=["Companies Endpoints"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    users.router,
    prefix=prefix,
    tags=["Users Endpoints"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    employees.router,
    prefix=prefix,
    tags=["Employees Endpoints"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    customers.router,
    prefix=prefix,
    tags=["Customers Endpoints"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    customer_employees.router,
    prefix=prefix,
    tags=["Customer Employees Endpoints"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    forwarders.router,
    prefix=prefix,
    tags=["Forwarders Endpoints"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    order.router,
    prefix=prefix,
    tags=["Orders Endpoints"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)
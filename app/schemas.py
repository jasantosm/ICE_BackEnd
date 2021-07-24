from typing import Optional
from datetime import date

from pydantic import BaseModel

class Company(BaseModel):
    id: int
    name: str
    email: str
    address: str
    city: str
    state: str
    phone: str
    logo: str
    vat_number: int

    class Config:
        orm_mode = True

class Customer(BaseModel):
    id: int
    name: str
    email: str
    address: str
    city: str
    state: str
    phone: str
    logo: str
    vat_number: int
    technical_advisor_id: int
    sales_advisor_id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    email: str
    password: str
    is_super = False
    is_admin = False
    is_customer = False
    is_ICE_admin = False

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Employee(BaseModel):
    id: int
    name: str
    phone: str
    whatsapp: str
    photo: str
    profession: str
    job_title: str
    about: str
    company_id: int
    user_id: int

    class Config:
        orm_mode = True

class CustomerEmployee(BaseModel):
    id: int
    name: str
    phone: str
    whatsapp: str
    photo: str
    job_title: str
    customer_id: int
    user_id: int

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    customer_number: int
    descripction: str
    order_date: date
    ETA: date
    amount: float
    terms: str
    forwarder_id: str
    tracking_code: str
    from_lat: float
    from_long: float
    to_lat: float
    to_long: float
    customer_id: int
    documents: str

    class Config:
        orm_mode = True

class Forwarder(BaseModel):
    id: int
    name: str
    phone: str
    extension: str
    contact_person_name: str
    cell_phone: str
    website: str

    class Config:
        orm_mode = True
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
    name: str
    phone: str
    whatsapp: Optional[str]
    photo: Optional[str]
    profession: Optional[str]
    job_title: str
    about: Optional[str]
    company_id: Optional[int]
    customer_id: Optional[int]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Order(BaseModel):
    id: int
    customer_number: int
    description: str
    order_date: date
    ETA: date
    amount: float
    terms: str
    forwarder_id: int
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
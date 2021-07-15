from typing import Optional

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

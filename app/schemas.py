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


class Employee(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    whatsapp:str
    password: str
    photo: str
    profession: str
    job_title: str
    is_admin: str
    is_assistant: str
    is_advisor: str
    companies_id: str
    about: str

    class Config:
        orm_mode = True


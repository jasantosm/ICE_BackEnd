from enum import unique
from sqlalchemy import Column, Integer, Text
from sqlalchemy.sql.sqltypes import Boolean

from .database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    logo = Column(Text, nullable=False)
    vat_number = Column(Integer, unique=True, nullable=False)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    logo = Column(Text, nullable=False)
    vat_number = Column(Integer, unique=True, nullable=False)
    technical_advisor_id = Column(Integer, nullable=False)
    sales_advisor_id = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    is_super = Column(Boolean, nullable=False,  default=False)
    is_admin = Column(Boolean, nullable=False,  default=False)
    is_customer = Column(Boolean, nullable=False,  default=False)
    is_ICE_admin = Column(Boolean, nullable=False,  default=False)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    whatsapp = Column(Text, nullable=True)
    photo = Column(Text, nullable=True)
    profession = Column(Text, nullable=False)
    job_title = Column(Text, nullable=False)
    about = Column(Text, nullable=True)
    company_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

class CustomerEmployee(Base):
    __tablename__ = "customer_employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    whatsapp = Column(Text, nullable=True)
    photo = Column(Text, nullable=True)
    job_title = Column(Text, nullable=False)
    customer_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

class Forwarder(Base):
    __tablename__ = "forwarders"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    extension = Column(Text, nullable=True)
    contact_person_name = Column(Text, nullable=False)
    cell_phone = Column(Text, nullable=True)
    website = Column(Text, nullable=True)
    
from datetime import date
from enum import unique
from sqlalchemy import Column, Integer, Text, Date, Float
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
    name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    whatsapp = Column(Text, nullable=True)
    photo = Column(Text, nullable=True)
    profession = Column(Text, nullable=True)
    job_title = Column(Text, nullable=False)
    about = Column(Text, nullable=True)
    company_id = Column(Integer, nullable=True)
    customer_id = Column(Integer, nullable=True)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    order_date = Column(Date, nullable=False)
    ETA = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    terms = Column(Text, nullable=False)
    forwarder_id = Column(Integer, nullable=False)
    tracking_code = Column(Text, nullable=True)
    from_lat = Column(Float, nullable=False)
    from_long = Column(Float, nullable=False)
    to_lat = Column(Float, nullable=False)
    to_long = Column(Float, nullable=False)
    customer_id = Column(Float, nullable=False)
    documents = Column(Text, nullable=True)

class Forwarder(Base):
    __tablename__ = "forwarders"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    extension = Column(Text, nullable=True)
    contact_person_name = Column(Text, nullable=False)
    cell_phone = Column(Text, nullable=True)
    website = Column(Text, nullable=True)
    
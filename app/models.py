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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    is_super = Column(Boolean, nullable=False,  default=False)
    is_admin = Column(Boolean, nullable=False,  default=False)
    is_customer = Column(Boolean, nullable=False,  default=False)
    is_ICE_admin = Column(Boolean, nullable=False,  default=False)
    
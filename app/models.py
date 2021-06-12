from enum import unique
from sqlalchemy import Column, Integer, Text

from .database import Base

class Company(Base):
    __tablename__ = "companies"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    logo = Column(Text, nullable=False)
    vat_number = Column(Integer, nullable=False)
    
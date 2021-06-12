import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@127.0.0.1:5432/ice_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
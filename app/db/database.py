from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  

engine = create_engine(DATABASE_URL, echo=True)  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Property(Base):
    __tablename__ = "Properties"
    
    id = Column(Integer, primary_key=True, index=True)
    building_name = Column(String(255), nullable=False)
    house_name = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    contract_start_date = Column(Date, nullable=False)
    contract_end_date = Column(Date, nullable=False)
    rent_price = Column(Numeric(10, 2), nullable=False)
    type = Column(String(50), nullable=False)
    total_rooms = Column(Integer, nullable=False)

def create_tables():
    Base.metadata.create_all(bind=engine)

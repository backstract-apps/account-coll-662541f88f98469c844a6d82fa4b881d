from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time, Float, Text, ForeignKey, JSON, Numeric, Date, TIMESTAMP, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employees(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, primary_key=False)
    employee_id = Column(String, primary_key=False)
    age = Column(Integer, primary_key=False)
    username = Column(String, primary_key=False)
    password = Column(String, primary_key=False)
    emailid = Column(String, primary_key=False)


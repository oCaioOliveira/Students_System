from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    addres = Column(String)
    neighbour = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String) 
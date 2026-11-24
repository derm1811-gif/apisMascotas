from sqlalchemy import Column, Integer, String
from database import Base

class Mascota(Base):
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    raza = Column(String, index=True)
    edad = Column(Integer, index=True)
    peso= Column(Integer, index=True)
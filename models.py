from sqlalchemy import Column, Integer, String
from database import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    especie = Column(String, index=True)
    raza = Column(String, index=True)
    edad = Column(Integer, index=True)
    peso= Column(Integer, index=True)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    correo = Column("email", String(320), nullable=False, unique=True, index=True)
    contrasena_hash = Column("contraseña", String(255), nullable=False)
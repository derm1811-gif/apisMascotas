import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
#traer la conexion de la base de datos desde el archivo .env
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,)

#sesiones
sesionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

#base de los modelos
Base = declarative_base()
def get_db():
    db = sesionLocal()
    try:
        yield db
    finally:
        db.close()
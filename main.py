from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Mascota as MascotaModel
from schemas import MascotaCreate, Mascota as MascotaSchema, MascotaDelete

#crear la base de datos
Base.metadata.create_all(bind=engine)
app = FastAPI(title="API de Mascotas")

#colsultar todas las mascotas
@app.get("/mascotas", response_model=list[MascotaSchema])
def get_mascotas(db: Session = Depends(get_db)):
    mascotas = db.query(MascotaModel).all()
    return mascotas

#colsultar una mascota por id
@app.get("/mascotas/{mascota_id}", response_model=MascotaSchema)
def get_mascota(
    mascota_id: int,
    db: Session = Depends(get_db)
    ):
    mascota = db.query(MascotaModel).filter(
        MascotaModel.id == mascota_id
        ).first()
    if mascota is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota

#registrar una mascota
@app.post("/mascotas", response_model=MascotaSchema, status_code=201)
def create_mascota(
    mascota: MascotaCreate,
    db: Session = Depends(get_db)
    ):
    db_mascota = MascotaModel(
        nombre=mascota.nombre,
        raza=mascota.raza,
        edad=mascota.edad,
        peso=mascota.peso
    )
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota


#actualizar una mascota
@app.put("/mascotas/{mascota_id}", response_model=MascotaSchema)
def update_mascota(
    mascota_id: int,
    mascota: MascotaCreate,
    db: Session = Depends(get_db)
):
    db_mascota = db.query(MascotaModel).filter(
        MascotaModel.id == mascota_id
    ).first()
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    for key, value in mascota.dict().items():
        setattr(db_mascota, key, value)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

#eliminar una mascota
@app.delete("/mascotas/{mascota_id}", response_model=MascotaDelete) 
def delete_mascota(
    mascota_id: int,
    db: Session = Depends(get_db)
):
    db_mascota = db.query(MascotaModel).filter(
        MascotaModel.id == mascota_id
    ).first()
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    db.delete(db_mascota)
    db.commit()
    return db_mascota
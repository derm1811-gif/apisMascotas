import base64
import hashlib
import secrets

from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Mascota as MascotaModel, Usuario as UsuarioModel
from schemas import (
    MascotaCreate,
    Mascota as MascotaSchema,
    MascotaDelete,
    UsuarioCreate,
    UsuarioSchema,
)

#crear la base de datos
Base.metadata.create_all(bind=engine)
app = FastAPI(title="API de Mascotas")


def hash_contrasena(contrasena: str) -> str:
    sal = secrets.token_bytes(16)
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode("utf-8"), sal, 600_000
    )
    return (
        f"pbkdf2_sha256$600000$"
        f"{base64.b64encode(sal).decode('ascii')}$"
        f"{base64.b64encode(hash_bytes).decode('ascii')}"
    )


@app.post("/usuarios/", response_model=UsuarioSchema, status_code=201)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(UsuarioModel).filter(
        UsuarioModel.correo == str(usuario.correo)
    ).first()
    if existente is not None:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")

    db_usuario = UsuarioModel(
        nombre=usuario.nombre,
        correo=str(usuario.correo),
        contrasena_hash=hash_contrasena(usuario.contrasena),
    )
    db.add(db_usuario)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="El correo ya está registrado"
        ) from error
    db.refresh(db_usuario)
    return db_usuario


@app.get("/usuarios/", response_model=list[UsuarioSchema])
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioModel).order_by(UsuarioModel.id).all()


@app.get("/usuarios/{usuario_id}", response_model=UsuarioSchema)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id
    ).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@app.put("/usuarios/{usuario_id}", response_model=UsuarioSchema)
def update_usuario(
    usuario_id: int,
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
):
    db_usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id
    ).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    existente = db.query(UsuarioModel).filter(
        UsuarioModel.correo == str(usuario.correo),
        UsuarioModel.id != usuario_id,
    ).first()
    if existente is not None:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")

    db_usuario.nombre = usuario.nombre
    db_usuario.correo = str(usuario.correo)
    db_usuario.contrasena_hash = hash_contrasena(usuario.contrasena)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="El correo ya está registrado"
        ) from error
    db.refresh(db_usuario)
    return db_usuario


@app.delete(
    "/usuarios/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id
    ).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#colsultar todas las mascotas
@app.get("/mascotas", response_model=list[MascotaSchema])
def get_mascotas(
    especie: str | None = None,
    db: Session = Depends(get_db)
):
    mascotas = db.query(MascotaModel)
    if especie is not None:
        mascotas = mascotas.filter(MascotaModel.especie.ilike(especie))
    mascotas = mascotas.all()
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
        especie=mascota.especie,
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
from pydantic import BaseModel,ConfigDict, EmailStr, Field

#crear mascota
class MascotaCreate(BaseModel):
    nombre: str=Field(min_length=1, max_length=50)
    raza: str=Field(min_length=1, max_length=50)
    edad: int=Field(ge=0)
    peso: int=Field(ge=0)

#devolver mascota
class Mascota(MascotaCreate):
    id: int
    nombre: str
    raza: str
    edad: int
    peso: int
    
    model_config = ConfigDict(from_attributes=True)

#elimiunar mascota
class MascotaDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
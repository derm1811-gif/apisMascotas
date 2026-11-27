from pydantic import BaseModel,ConfigDict, EmailStr, Field, field_validator

#crear mascota
class MascotaCreate(BaseModel):
    nombre: str=Field(min_length=1, max_length=50)
    especie: str=Field(min_length=1, max_length=50)
    raza: str=Field(min_length=1, max_length=50)
    edad: int=Field(ge=0)
    peso: int=Field(ge=0)

#devolver mascota
class Mascota(MascotaCreate):
    id: int
    nombre: str
    especie: str
    raza: str
    edad: int
    peso: int
    
    model_config = ConfigDict(from_attributes=True)

#elimiunar mascota
class MascotaDelete(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=128)

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre es obligatorio")
        return value

    @field_validator("correo", mode="before")
    @classmethod
    def normalizar_correo(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().lower()
        return value


class UsuarioSchema(BaseModel):
    id: int
    nombre: str
    correo: EmailStr

    model_config = ConfigDict(from_attributes=True)
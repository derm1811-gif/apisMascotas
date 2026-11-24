# API de Mascotas

Proyecto de Daniel Enrique Racero Mendoza para registrar y administrar mascotas de un centro de protección animal. Está desarrollado con FastAPI, SQLAlchemy y PostgreSQL.

## Datos de una mascota

- `id`: identificador generado por la base de datos.
- `nombre`: nombre de la mascota.
- `especie`: especie, por ejemplo, perro o gato.
- `raza`: raza de la mascota.
- `edad`: edad en años.
- `peso`: peso.

## Requisitos

- Python 3.10 o superior.
- PostgreSQL; el proyecto puede conectarse a una base de datos alojada en Neon.

## Instalación y ejecución

En PowerShell, desde la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz y configura la URL de conexión de PostgreSQL:

```env
DATABASE_URL=postgresql+psycopg://USUARIO:CONTRASENA@HOST/BASE_DE_DATOS?sslmode=require
```

No compartas ni subas el archivo `.env`; contiene credenciales. Luego inicia la API:

```powershell
uvicorn main:app --reload
```

La documentación interactiva estará en <http://127.0.0.1:8000/docs>.

## Endpoints

| Método | Ruta | Función |
|---|---|---|
| `POST` | `/mascotas` | Registrar una mascota. |
| `GET` | `/mascotas` | Consultar todas las mascotas. |
| `GET` | `/mascotas?especie=Perro` | Filtrar mascotas por especie. |
| `GET` | `/mascotas/{mascota_id}` | Consultar una mascota por ID. |
| `PUT` | `/mascotas/{mascota_id}` | Actualizar una mascota. |
| `DELETE` | `/mascotas/{mascota_id}` | Eliminar una mascota. |

Para registrar o actualizar, envía un JSON como:

```json
{
  "nombre": "Luna",
  "especie": "Gato",
  "raza": "Criolla",
  "edad": 3,
  "peso": 4
}
```

Las validaciones exigen nombre, especie y raza de 1 a 50 caracteres, y edad y peso mayores o iguales a cero. Las rutas por ID responden con error `404` cuando la mascota no existe.

## Organización del código

- `main.py`: rutas HTTP y operaciones CRUD.
- `models.py`: modelo de SQLAlchemy y tabla `mascotas`.
- `schemas.py`: validación de datos y formato de respuestas con Pydantic.
- `database.py`: conexión, sesiones y dependencia de base de datos.
- `requirements.txt`: dependencias de Python.

Las rutas realizan directamente las consultas usando el modelo ORM; el proyecto no cuenta actualmente con capas separadas de servicios o repositorios. `Base.metadata.create_all()` crea tablas que no existan, pero no modifica tablas existentes; si la tabla ya estaba creada, agrega la columna `especie` mediante una migración o cambio en PostgreSQL.

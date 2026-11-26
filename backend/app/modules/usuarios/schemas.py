from pydantic import BaseModel, EmailStr

from app.modules.usuarios.models import EstadoUsuario


class UsuarioCreate(BaseModel):
    rol_uuid: str
    numero_empleado: str | None = None
    nombre: str
    apellido: str
    correo: EmailStr
    contrasena: str
    telefono: str | None = None


class UsuarioUpdate(BaseModel):
    rol_uuid: str | None = None
    numero_empleado: str | None = None
    nombre: str | None = None
    apellido: str | None = None
    telefono: str | None = None
    estado: EstadoUsuario | None = None


class UsuarioResponse(BaseModel):
    uuid: str
    numero_empleado: str | None
    nombre: str
    apellido: str
    correo: EmailStr
    telefono: str | None
    estado: EstadoUsuario
    rol: str
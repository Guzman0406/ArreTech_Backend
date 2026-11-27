from pydantic import BaseModel, EmailStr


class ClienteCreate(BaseModel):
    nombre: str
    telefono: str | None = None
    correo: EmailStr | None = None


class ClienteUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    correo: EmailStr | None = None


class ClienteResponse(BaseModel):
    uuid: str
    nombre: str
    telefono: str | None
    correo: EmailStr | None
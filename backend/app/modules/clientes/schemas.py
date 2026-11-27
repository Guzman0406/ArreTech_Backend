from pydantic import BaseModel, Emailstr


class ClienteCreate(BaseModel):
    nombre: str
    telefono: str | None = None
    correo: Emailstr | None = None


class ClienteUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    correo: Emailstr | None = None


class ClienteResponse(BaseModel):
    uuid: str
    nombre: str
    telefono: str | None
    correo: Emailstr | None
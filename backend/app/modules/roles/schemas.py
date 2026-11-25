from pydantic import BaseModel


class RolCreate(BaseModel):
    nombre: str
    descripcion: str | None = None


class RolResponse(BaseModel):
    uuid: str
    nombre: str
    descripcion: str | None = None
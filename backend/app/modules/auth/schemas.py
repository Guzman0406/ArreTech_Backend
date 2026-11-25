from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str


class UsuarioLoginInfo(BaseModel):
    uuid: str
    nombre: str
    apellido: str
    correo: EmailStr
    rol: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioLoginInfo
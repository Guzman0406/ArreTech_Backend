from dataclasses import dataclass

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decodificar_access_token
from app.modules.usuarios.models import EstadoUsuario, Usuario


@dataclass
class UsuarioActual:
    usuario: Usuario
    rol: str


async def obtener_usuario_actual(
    authorization: str = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> UsuarioActual:
    if authorization is None or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Falta el token de autenticación")

    token = authorization.removeprefix("Bearer ").strip()
    payload = decodificar_access_token(token)

    usuario_uuid = payload.get("sub")
    rol = payload.get("rol")

    stmt = select(Usuario).where(Usuario.uuid == usuario_uuid, Usuario.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    usuario = resultado.scalar_one_or_none()

    if usuario is None or usuario.estado != EstadoUsuario.activo:
        raise UnauthorizedError("El usuario ya no existe o está inactivo")

    return UsuarioActual(usuario=usuario, rol=rol)


def requiere_rol(*roles_permitidos: str):
    async def verificador(actual: UsuarioActual = Depends(obtener_usuario_actual)) -> UsuarioActual:
        if actual.rol not in roles_permitidos:
            raise ForbiddenError("No tienes permiso para realizar esta acción")
        return actual

    return verificador
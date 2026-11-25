from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import crear_access_token, verificar_contrasena
from app.modules.auth.schemas import LoginRequest, LoginResponse, UsuarioLoginInfo
from app.modules.roles.repository import obtener_rol_por_id
from app.modules.usuarios.models import EstadoUsuario
from app.modules.usuarios.repository import obtener_usuario_por_correo

async def iniciar_sesion(db: AsyncSession, datos: LoginRequest) -> LoginResponse:
    
    usuario = await obtener_usuario_por_correo(db, datos.correo)

    if usuario is None or not verificar_contrasena(datos.contrasena, usuario.contrasena_hash):
        raise UnauthorizedError("Correo o contraseña incorrectos")

    if usuario.estado != EstadoUsuario.activo:
        raise UnauthorizedError("Correo o contraseña incorrectos")

    rol = await obtener_rol_por_id(db, usuario.id_rol)

    token = crear_access_token(str(usuario.uuid), rol.nombre)

    return LoginResponse(
        access_token=token,
        usuario=UsuarioLoginInfo(
            uuid=str(usuario.uuid),
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            correo=usuario.correo,
            rol=rol.nombre

        ),
    )
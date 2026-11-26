from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hashear_contrasena
from app.modules.roles.repository import obtener_rol_por_id, obtener_rol_por_uuid
from app.modules.usuarios.repository import (
    actualizar_usuario,
    crear_usuario,
    listar_usuarios,
    obtener_usuario_por_correo,
    obtener_usuario_por_numero_empleado,
    obtener_usuario_por_uuid,
)
from app.modules.usuarios.schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate


def _a_respuesta(usuario, rol_nombre: str) -> UsuarioResponse:
    return UsuarioResponse(
        uuid=str(usuario.uuid),
        numero_empleado=usuario.numero_empleado,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        telefono=usuario.telefono,
        estado=usuario.estado,
        rol=rol_nombre,
    )


async def listar(db: AsyncSession) -> list[UsuarioResponse]:
    usuarios = await listar_usuarios(db)
    resultado = []
    for usuario in usuarios:
        rol = await obtener_rol_por_id(db, usuario.id_rol)
        resultado.append(_a_respuesta(usuario, rol.nombre))
    return resultado


async def obtener(db: AsyncSession, usuario_uuid: str) -> UsuarioResponse:
    usuario = await obtener_usuario_por_uuid(db, usuario_uuid)
    if usuario is None:
        raise NotFoundError("Usuario no encontrado")

    rol = await obtener_rol_por_id(db, usuario.id_rol)
    return _a_respuesta(usuario, rol.nombre)


async def crear(db: AsyncSession, datos: UsuarioCreate) -> UsuarioResponse:
    rol = await obtener_rol_por_uuid(db, datos.rol_uuid)
    if rol is None:
        raise NotFoundError("El rol indicado no existe")

    if await obtener_usuario_por_correo(db, datos.correo) is not None:
        raise ConflictError("Ya existe un usuario con ese correo")

    if datos.numero_empleado is not None:
        if await obtener_usuario_por_numero_empleado(db, datos.numero_empleado) is not None:
            raise ConflictError("Ya existe un usuario con ese numero de empleado")

    contrasena_hash = hashear_contrasena(datos.contrasena)

    usuario = await crear_usuario(
        db,
        id_rol=rol.id,
        numero_empleado=datos.numero_empleado,
        nombre=datos.nombre,
        apellido=datos.apellido,
        correo=datos.correo,
        contrasena_hash=contrasena_hash,
        telefono=datos.telefono,
    )

    return _a_respuesta(usuario, rol.nombre)


async def actualizar(db: AsyncSession, usuario_uuid: str, datos: UsuarioUpdate) -> UsuarioResponse:
    usuario = await obtener_usuario_por_uuid(db, usuario_uuid)
    if usuario is None:
        raise NotFoundError("Usuario no encontrado")

    cambios = {}

    if datos.rol_uuid is not None:
        rol_nuevo = await obtener_rol_por_uuid(db, datos.rol_uuid)
        if rol_nuevo is None:
            raise NotFoundError("El rol indicado no existe")
        cambios["id_rol"] = rol_nuevo.id

    if datos.numero_empleado is not None:
        existente = await obtener_usuario_por_numero_empleado(db, datos.numero_empleado)
        if existente is not None and existente.id != usuario.id:
            raise ConflictError("Ya existe un usuario con ese numero de empleado")
        cambios["numero_empleado"] = datos.numero_empleado

    if datos.nombre is not None:
        cambios["nombre"] = datos.nombre
    if datos.apellido is not None:
        cambios["apellido"] = datos.apellido
    if datos.telefono is not None:
        cambios["telefono"] = datos.telefono
    if datos.estado is not None:
        cambios["estado"] = datos.estado

    usuario = await actualizar_usuario(db, usuario, cambios)

    rol = await obtener_rol_por_id(db, usuario.id_rol)
    return _a_respuesta(usuario, rol.nombre)
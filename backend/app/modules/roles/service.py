from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.modules.roles.repository import crear_rol, listar_roles, obtener_rol_por_nombre
from app.modules.roles.schemas import RolCreate, RolResponse


async def listar(db: AsyncSession) -> list[RolResponse]:
    roles = await listar_roles(db)
    return [RolResponse(uuid=str(r.uuid), nombre=r.nombre, descripcion=r.descripcion) for r in roles]


async def crear(db: AsyncSession, datos: RolCreate) -> RolResponse:
    existente = await obtener_rol_por_nombre(db, datos.nombre)
    if existente is not None:
        raise ConflictError("Ya existe un rol con ese nombre")

    rol = await crear_rol(db, datos.nombre, datos.descripcion)
    return RolResponse(uuid=str(rol.uuid), nombre=rol.nombre, descripcion=rol.descripcion)
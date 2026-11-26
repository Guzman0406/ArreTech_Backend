from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.roles.models import Rol


async def obtener_rol_por_id(db: AsyncSession, id_rol: int) -> Rol | None:
    stmt = select(Rol).where(Rol.id == id_rol, Rol.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()
    

async def obtener_rol_por_nombre(db: AsyncSession, nombre: str) -> Rol | None:
    stmt = select(Rol).where(Rol.nombre == nombre, Rol.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def listar_roles(db: AsyncSession) -> list[Rol]:
    stmt = select(Rol).where(Rol.deleted_at.is_(None)).order_by(Rol.nombre)
    resultado = await db.execute(stmt)
    return list(resultado.scalars().all())


async def crear_rol(db: AsyncSession, nombre: str, descripcion: str | None) -> Rol:
    rol = Rol(nombre=nombre, descripcion=descripcion)
    db.add(rol)
    await db.commit()
    await db.refresh(rol)
    return rol

async def obtener_rol_por_uuid(db: AsyncSession, rol_uuid: str) -> Rol | None:
    stmt = select(Rol).where(Rol.uuid == rol_uuid, Rol.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()
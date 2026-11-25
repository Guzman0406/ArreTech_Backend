from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.roles.models import Rol


async def obtener_rol_por_id(db: AsyncSession, id_rol: int) -> Rol | None:
    stmt = select(Rol).where(Rol.id == id_rol, Rol.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()
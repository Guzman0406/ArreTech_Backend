from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.usuarios.models import Usuario


async def obtener_usuario_por_correo(db: AsyncSession, correo: str) -> Usuario | None:
    stmt = select(Usuario).where(Usuario.correo == correo, Usuario.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()
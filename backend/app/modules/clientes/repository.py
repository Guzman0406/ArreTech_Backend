from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.clientes.models import Cliente

async def obtener_cliente_por_uuid(db: AsyncSession, cliente_uuid: str) -> Cliente | None:
    stmt = select(Cliente).where(Cliente.uuid == cliente_uuid, Cliente.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def obtener_cliente_por_telefono(db: AsyncSession, telefono: str) -> Cliente | None:
    stmt = select(Cliente).where(Cliente.telefono == telefono, Cliente.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def obtener_cliente_por_correo(db: AsyncSession, correo: str) -> Cliente | None:
    stmt = select(Cliente).where(Cliente.correo == correo, Cliente.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def listar_clientes(db: AsyncSession) -> list[Cliente]:
    stmt = select(Cliente).where(Cliente.deleted_at.is_(None)).order_by(Cliente.nombre)
    resultado = await db.execute(stmt)
    return list(resultado.scalars().all())


async def crear_cliente(
    db: AsyncSession,
    *,
    nombre: str,
    telefono: str | None,
    correo: str | None,
) -> Cliente:
    cliente = Cliente(nombre=nombre, telefono=telefono, correo=correo)
    db.add(cliente)
    await db.commit()
    await db.refresh(cliente)
    return cliente


async def actualizar_cliente(db: AsyncSession, cliente: Cliente, cambios: dict) -> Cliente:
    for campo, valor in cambios.items():
        setattr(cliente, campo, valor)
    await db.commit()
    await db.refresh(cliente)
    return cliente
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.productos.models import Producto

async def obtener_producto_por_nombre(db: AsyncSession, nombre: str) -> Producto | None:
    stmt = select(Producto).where(Producto.nombre == nombre, Producto.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def obtener_producto_por_uuid(db: AsyncSession, producto_uuid: str) -> Producto | None: 
    stmt = select(Producto).where(Producto.uuid == producto_uuid, Producto.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def listar_productos(db: AsyncSession) -> list[Producto]:
    stmt = select(Producto).where(Producto.deleted_at.is_(None)).order_by(Producto.nombre)
    resultado = await db.execute(stmt)
    return list(resultado.scalars().all())

async def crear_producto(
    db: AsyncSession,
    *, 
    nombre: str,
    descripcion: str | None,
    categoria: str | None,
    precio: Decimal,
    stock_actual: int,
    stock_minimo: int,
) -> Producto:
    producto  = Producto(
        nombre = nombre,
        descripcion = descripcion,
        categoria = categoria,
        precio = precio,
        stock_actual = stock_actual,
        stock_minimo = stock_minimo,
    )
    db.add(producto)
    await db.commit()
    await db.refresh(producto)
    return producto


async def actualizar_producto(db: AsyncSession, producto: Producto, cambios: dict) -> Producto:
    for campo, valor in cambios.items():
        setattr(producto, campo, valor)
    await db.commit()
    await db.refresh(producto)
    return producto
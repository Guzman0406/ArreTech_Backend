from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.modules.productos.repository import (
    actualizar_producto,
    crear_producto,
    listar_productos,
    obtener_producto_por_nombre,
    obtener_producto_por_uuid,
)
from app.modules.productos.schemas import ProductoCreate, ProductoResponse, ProductoUpdate


def _a_respuesta(producto)->ProductoResponse:
    return ProductoResponse(
        uuid=str(producto.uuid),
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        categoria=producto.categoria,
        precio=producto.precio,
        stock_actual=producto.stock_actual,
        stock_minimo=producto.stock_minimo,
    )


async def listar(db: AsyncSession) -> list[ProductoResponse]:
    productos = await listar_productos(db)
    return [_a_respuesta(p) for p in productos]


async def obtener(db: AsyncSession, producto_uuid: str) -> ProductoResponse:
    producto = await obtener_producto_por_uuid(db, producto_uuid)
    if producto is None:
        raise NotFoundError("Producto no encontrado")

    return _a_respuesta(producto)


async def crear(db: AsyncSession, datos: ProductoCreate) -> ProductoResponse:
    if await obtener_producto_por_nombre(db, datos.nombre) is not None:
        raise ConflictError("Ya existe un producto con ese nombre")

    producto = await crear_producto(
        db,
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        categoria=datos.categoria,
        precio=datos.precio,
        stock_actual=datos.stock_actual,
        stock_minimo=datos.stock_minimo,
    )

    return _a_respuesta(producto)


async def actualizar(db: AsyncSession, producto_uuid: str, datos: ProductoUpdate) -> ProductoResponse:
    producto = await obtener_producto_por_uuid(db, producto_uuid)
    if producto is None:
        raise NotFoundError("Producto no encontrado")

    cambios = {}

    if datos.nombre is not None and datos.nombre != producto.nombre:
        existente = await obtener_producto_por_nombre(db, datos.nombre)
        if existente is not None and existente.id != producto.id:
            raise ConflictError("Ya existe un producto con ese nombre")
        cambios["nombre"] = datos.nombre

    if datos.descripcion is not None:
        cambios["descripcion"] = datos.descripcion
    if datos.categoria is not None:
        cambios["categoria"] = datos.categoria
    if datos.precio is not None:
        cambios["precio"] = datos.precio
    if datos.stock_minimo is not None:
        cambios["stock_minimo"] = datos.stock_minimo

    producto = await actualizar_producto(db, producto, cambios)

    return _a_respuesta(producto)

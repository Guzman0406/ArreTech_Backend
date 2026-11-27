from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import obtener_usuario_actual, requiere_rol
from app.core.responses import success_response
from app.modules.productos.schemas import ProductoCreate, ProductoUpdate
from app.modules.productos.service import actualizar, crear, listar, obtener

router = APIRouter(prefix="/api/v1/productos", tags=["Productos"])


@router.get("", dependencies=[Depends(obtener_usuario_actual)])
async def listar_productos_endpoint(db: AsyncSession = Depends(get_db)):
    resultado = await listar(db)
    return success_response(data=[p.model_dump() for p in resultado])


@router.get("/{producto_uuid}", dependencies=[Depends(obtener_usuario_actual)])
async def obtener_producto_endpoint(
    producto_uuid: str,
    db: AsyncSession = Depends(get_db),
):
    resultado = await obtener(db, producto_uuid)
    return success_response(data=resultado.model_dump())


@router.post("", dependencies=[Depends(requiere_rol("Administrador"))])
async def crear_producto_endpoint(
    datos: ProductoCreate,
    db: AsyncSession = Depends(get_db),
):
    resultado = await crear(db, datos)
    return success_response(data=resultado.model_dump())


@router.patch("/{producto_uuid}", dependencies=[Depends(requiere_rol("Administrador"))])
async def actualizar_producto_endpoint(
    producto_uuid: str,
    datos: ProductoUpdate,
    db: AsyncSession = Depends(get_db),
):
    resultado = await actualizar(db, producto_uuid, datos)
    return success_response(data=resultado.model_dump())
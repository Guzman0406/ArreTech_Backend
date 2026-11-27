from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import requiere_rol
from app.core.responses import success_response
from app.modules.clientes.schemas import ClienteCreate, ClienteUpdate
from app.modules.clientes.service import actualizar, crear, listar, obtener

router = APIRouter(prefix="/api/v1/clientes", tags=["Clientes"])


@router.get("", dependencies=[Depends(requiere_rol("Administrador", "Ventas/Caja", "Técnicos"))])
async def listar_clientes_endpoint(db: AsyncSession = Depends(get_db)):
    resultado = await listar(db)
    return success_response(data=[c.model_dump() for c in resultado])


@router.get("/{cliente_uuid}", dependencies=[Depends(requiere_rol("Administrador", "Ventas/Caja", "Técnicos"))])
async def obtener_cliente_endpoint(
    cliente_uuid: str,
    db: AsyncSession = Depends(get_db),
):
    resultado = await obtener(db, cliente_uuid)
    return success_response(data=resultado.model_dump())


@router.post("", dependencies=[Depends(requiere_rol("Administrador", "Ventas/Caja"))])
async def crear_cliente_endpoint(
    datos: ClienteCreate,
    db: AsyncSession = Depends(get_db),
):
    resultado = await crear(db, datos)
    return success_response(data=resultado.model_dump())


@router.patch("/{cliente_uuid}", dependencies=[Depends(requiere_rol("Administrador", "Ventas/Caja"))])
async def actualizar_cliente_endpoint(
    cliente_uuid: str,
    datos: ClienteUpdate,
    db: AsyncSession = Depends(get_db),
):
    resultado = await actualizar(db, cliente_uuid, datos)
    return success_response(data=resultado.model_dump())
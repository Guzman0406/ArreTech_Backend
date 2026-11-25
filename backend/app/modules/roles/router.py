from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import requiere_rol
from app.core.responses import success_response
from app.modules.roles.schemas import RolCreate
from app.modules.roles.service import crear, listar

router = APIRouter(prefix="/api/v1/roles", tags=["Roles"])


@router.get("", dependencies=[Depends(requiere_rol("Administrador"))])
async def listar_roles_endpoint(db: AsyncSession = Depends(get_db)):
    resultado = await listar(db)
    return success_response(data=[r.model_dump() for r in resultado])


@router.post("", dependencies=[Depends(requiere_rol("Administrador"))])
async def crear_rol_endpoint(
    datos: RolCreate,
    db: AsyncSession = Depends(get_db),
):
    resultado = await crear(db, datos)
    return success_response(data=resultado.model_dump())
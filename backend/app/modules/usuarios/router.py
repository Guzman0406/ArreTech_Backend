from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import requiere_rol
from app.core.responses import success_response
from app.modules.usuarios.schemas import UsuarioCreate, UsuarioUpdate
from app.modules.usuarios.service import actualizar, crear, listar, obtener

router = APIRouter(
    prefix="/api/v1/usuarios",
    tags=["Usuarios"],
    dependencies=[Depends(requiere_rol("Administrador"))],
)


@router.get("")
async def listar_usuarios_endpoint(db: AsyncSession = Depends(get_db)):
    resultado = await listar(db)
    return success_response(data=[u.model_dump() for u in resultado])


@router.post("")
async def crear_usuario_endpoint(
    datos: UsuarioCreate,
    db: AsyncSession = Depends(get_db),
):
    resultado = await crear(db, datos)
    return success_response(data=resultado.model_dump())


@router.get("/{usuario_uuid}")
async def obtener_usuario_endpoint(
    usuario_uuid: str,
    db: AsyncSession = Depends(get_db),
):
    resultado = await obtener(db, usuario_uuid)
    return success_response(data=resultado.model_dump())


@router.patch("/{usuario_uuid}")
async def actualizar_usuario_endpoint(
    usuario_uuid: str,
    datos: UsuarioUpdate,
    db: AsyncSession = Depends(get_db),
):
    resultado = await actualizar(db, usuario_uuid, datos)
    return success_response(data=resultado.model_dump())
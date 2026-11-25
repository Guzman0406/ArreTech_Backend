from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.responses import success_response
from app.modules.auth.schemas import LoginRequest
from app.modules.auth.service import iniciar_sesion

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/login")
async def login(
    datos: LoginRequest, 
    db: AsyncSession = Depends(get_db),
):

    resultado = await iniciar_sesion(db, datos)
    return success_response(data=resultado.model_dump())
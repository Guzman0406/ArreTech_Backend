from fastapi import FastAPI

from app.core.error_handlers import register_error_handlers
from app.modules.auth.router import router as auth_router
from app.modules.roles.router import router as roles_router
from app.modules.usuarios.router import router as usuarios_router
from app.modules.productos.router import router as productos_router

app = FastAPI(
    title="ArreTech API",
    description="API con autenticación para el control de inventario y reparaciones de ArreTech.",
    version="0.1.0",
)

register_error_handlers(app)
app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(usuarios_router)
app.include_router(productos_router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
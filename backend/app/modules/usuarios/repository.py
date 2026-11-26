from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.modules.usuarios.models import Usuario


async def obtener_usuario_por_correo(db: AsyncSession, correo: str) -> Usuario | None:
    stmt = select(Usuario).where(Usuario.correo == correo, Usuario.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def obtener_usuario_por_numero_empleado(db: AsyncSession, numero_empleado: str) -> Usuario | None:
    stmt = select(Usuario).where(Usuario.numero_empleado == numero_empleado, Usuario.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def obtener_usuario_por_uuid(db: AsyncSession, usuario_uuid: str) -> Usuario | None:
    stmt = select(Usuario).where(Usuario.uuid == usuario_uuid, Usuario.deleted_at.is_(None))
    resultado = await db.execute(stmt)
    return resultado.scalar_one_or_none()


async def listar_usuarios(db: AsyncSession) -> list[Usuario]:
    stmt = select(Usuario).where(Usuario.deleted_at.is_(None)).order_by(Usuario.nombre)
    resultado = await db.execute(stmt)
    return list(resultado.scalars().all())


async def crear_usuario(
    db: AsyncSession,
    *,
    id_rol: int,
    numero_empleado: str | None,
    nombre: str,
    apellido: str,
    correo: str,
    contrasena_hash: str,
    telefono: str | None,
) -> Usuario:
    usuario = Usuario(
        id_rol=id_rol,
        numero_empleado=numero_empleado,
        nombre=nombre,
        apellido=apellido,
        correo=correo,
        contrasena_hash=contrasena_hash,
        telefono=telefono,
    )
    db.add(usuario)
    await db.commit()
    await db.refresh(usuario)
    return usuario


async def actualizar_usuario(db: AsyncSession, usuario: Usuario, cambios: dict) -> Usuario:
    for campo, valor in cambios.items():
        setattr(usuario, campo, valor)
    await db.commit()
    await db.refresh(usuario)
    return usuario
    

async def eliminar_usuario(db: AsyncSession, usuario: Usuario) -> None:
    usuario.deleted_at = datetime.now(timezone.utc)
    await db.commit()
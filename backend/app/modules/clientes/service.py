from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.modules.clientes.repository import (
    actualizar_cliente,
    crear_cliente,
    listar_clientes,
    obtener_cliente_por_correo,
    obtener_cliente_por_telefono,
    obtener_cliente_por_uuid,
)
from app.modules.clientes.schemas import ClienteCreate, ClienteResponse, ClienteUpdate


def _a_respuesta(cliente) -> ClienteResponse:
    return ClienteResponse(
        uuid=str(cliente.uuid),
        nombre=cliente.nombre,
        telefono=cliente.telefono,
        correo=cliente.correo,
    )

async def listar(db: AsyncSession) -> list[ClienteResponse]:
    clientes = await listar_clientes(db)
    return [_a_respuesta(c) for c in clientes]


async def obtener(db: AsyncSession, cliente_uuid: str) -> ClienteResponse:
    cliente = await obtener_cliente_por_uuid(db, cliente_uuid)
    if cliente is None:
        raise NotFoundError("Cliente no encontrado")
    return _a_respuesta(cliente)


async def crear(db: AsyncSession, datos: ClienteCreate) -> ClienteResponse:
    if datos.telefono is None and datos.correo is None:
        raise BadRequestError("El cliente debe tener al menos telefono o correo")

    if datos.telefono is not None and await obtener_cliente_por_telefono(db, datos.telefono) is not None:
        raise ConflictError("Ya existe un cliente con ese telefono")

    if datos.correo is not None and await obtener_cliente_por_correo(db, datos.correo) is not None:
        raise ConflictError("Ya existe un cliente con ese correo")

    cliente = await crear_cliente(
        db,
        nombre=datos.nombre,
        telefono=datos.telefono,
        correo=datos.correo,
    )

    return _a_respuesta(cliente)


async def actualizar(db: AsyncSession, cliente_uuid: str, datos: ClienteUpdate) -> ClienteResponse:
    cliente = await obtener_cliente_por_uuid(db, cliente_uuid)
    if cliente is None:
        raise NotFoundError("Cliente no encontrado")

    cambios = {}

    if datos.telefono is not None:
        existente = await obtener_cliente_por_telefono(db, datos.telefono)
        if existente is not None and existente.id != cliente.id:
            raise ConflictError("Ya existe un cliente con ese telefono")
        cambios["telefono"] = datos.telefono

    if datos.correo is not None:
        existente = await obtener_cliente_por_correo(db, datos.correo)
        if existente is not None and existente.id != cliente.id:
            raise ConflictError("Ya existe un cliente con ese correo")
        cambios["correo"] = datos.correo

    telefono_final = cambios.get("telefono", cliente.telefono)
    correo_final = cambios.get("correo", cliente.correo)
    if telefono_final is None and correo_final is None:
        raise BadRequestError("El cliente debe tener al menos telefono o correo")

    if datos.nombre is not None:
        cambios["nombre"] = datos.nombre

    cliente = await actualizar_cliente(db, cliente, cambios)

    return _a_respuesta(cliente)


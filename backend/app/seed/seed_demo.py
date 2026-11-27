import asyncio

from app.core.database import AsyncSessionLocal
from app.core.security import hashear_contrasena
from app.modules.roles.repository import crear_rol, obtener_rol_por_nombre
from app.modules.usuarios.repository import crear_usuario, obtener_usuario_por_correo

ROLES = [
    ("Administrador", "Acceso total: crea usuarios y productos, consulta auditoria, y tambien puede vender y atender tickets."),
    ("Bodega", "Registra entradas y salidas de inventario con precios ya puestos por el Admin."),
    ("Ventas/Caja", "Registra clientes, abre tickets en recepcion, vende piezas directo y marca tickets como entregados."),
    ("Técnicos", "Diagnostica, repara, agrega piezas al ticket y pone evidencias."),
]

USUARIOS = [
    {
        "rol": "Administrador",
        "numero_empleado": "EMP-001",
        "nombre": "Admin",
        "apellido": "Demo",
        "correo": "admin@arretech.test",
        "contrasena": "243715",
        "telefono": None,
    },
    {
        "rol": "Ventas/Caja",
        "numero_empleado": "EMP-002",
        "nombre": "Caja",
        "apellido": "Demo",
        "correo": "ventas@arretech.test",
        "contrasena": "243681",
        "telefono": None,
    },
    {
        "rol": "Bodega",
        "numero_empleado": "EMP-003",
        "nombre": "Bodega",
        "apellido": "Demo",
        "correo": "bodega@arretech.test",
        "contrasena": "fercho123",
        "telefono": None,
    },
    {
        "rol": "Técnicos",
        "numero_empleado": "EMP-004",
        "nombre": "Tecnico",
        "apellido": "Demo",
        "correo": "tecnico@arretech.test",
        "contrasena": "fercho123",
        "telefono": None,
    },
]


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        roles_por_nombre = {}

        for nombre, descripcion in ROLES:
            rol = await obtener_rol_por_nombre(db, nombre)
            if rol is None:
                rol = await crear_rol(db, nombre, descripcion)
                print(f"Rol creado: {nombre}")
            else:
                print(f"Rol ya existia: {nombre}")
            roles_por_nombre[nombre] = rol

        for datos in USUARIOS:
            existente = await obtener_usuario_por_correo(db, datos["correo"])
            if existente is not None:
                print(f"Usuario ya existia: {datos['correo']}")
                continue

            rol = roles_por_nombre[datos["rol"]]
            contrasena_hash = hashear_contrasena(datos["contrasena"])

            await crear_usuario(
                db,
                id_rol=rol.id,
                numero_empleado=datos["numero_empleado"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                correo=datos["correo"],
                contrasena_hash=contrasena_hash,
                telefono=datos["telefono"],
            )
            print(f"Usuario creado: {datos['correo']} ({datos['rol']})")


if __name__ == "__main__":
    asyncio.run(seed())
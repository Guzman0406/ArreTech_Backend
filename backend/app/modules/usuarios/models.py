import enum

from sqlalchemy import Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import BaseModelMixin
from app.core.database import Base


class EstadoUsuario(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"


class Usuario(Base, BaseModelMixin):
    __tablename__ = "usuarios"

    id_rol: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    numero_empleado: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    correo: Mapped[str] = mapped_column(String(255), nullable=False)
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    estado: Mapped[EstadoUsuario] = mapped_column(
        Enum(EstadoUsuario, name="estado_usuario"),
        nullable=False,
        default=EstadoUsuario.activo,
        server_default=EstadoUsuario.activo.value,
    )

    __table_args__ = (
        Index(
            "ix_usuarios_correo_activo",
            "correo",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
        Index(
            "ix_usuarios_numero_empleado_activo",
            "numero_empleado",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
    )
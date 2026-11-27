import enum

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import BaseModelMixin
from app.core.database import Base


class TipoMovimiento(str, enum.Enum):
    entrada = "entrada"
    salida = "salida"


class MovimientoInventario(Base, BaseModelMixin):
    __tablename__ = "movimientos_inventario"

    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("productos.id"), nullable=False)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_movimiento: Mapped[TipoMovimiento] = mapped_column(
        Enum(TipoMovimiento, name="tipo_movimiento"),
        nullable=False,
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    referencia: Mapped[str | None] = mapped_column(String(150), nullable=True)

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_movimientos_cantidad_positiva"),
    )
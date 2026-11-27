from decimal import Decimal

from sqlalchemy import CheckConstraint, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import BaseModelMixin
from app.core.database import Base


class Producto(Base, BaseModelMixin):
    __tablename__ = "productos"

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    categoria: Mapped[str | None] = mapped_column(String(100), nullable=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock_actual: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    stock_minimo: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    __table_args__ = (
        CheckConstraint("precio >= 0", name="ck_productos_precio_no_negativo"),
        CheckConstraint("stock_actual >= 0", name="ck_productos_stock_actual_no_negativo"),
        CheckConstraint("stock_minimo >= 0", name="ck_productos_stock_minimo_no_negativo"),
        Index(
            "ix_productos_nombre_activo",
            "nombre",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
    )
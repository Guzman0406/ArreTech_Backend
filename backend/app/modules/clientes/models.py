from sqlalchemy import CheckConstraint, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import BaseModelMixin
from app.core.database import Base


class Cliente(Base, BaseModelMixin):
    __tablename__ = "clientes"

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    correo: Mapped[str | None] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "telefono IS NOT NULL OR correo IS NOT NULL",
            name="ck_clientes_telefono_o_correo",
        ),
        Index(
            "ix_clientes_telefono_activo",
            "telefono",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
        Index(
            "ix_clientes_correo_activo",
            "correo",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
    )
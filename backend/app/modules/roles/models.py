from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import BaseModelMixin
from app.core.database import Base


class Rol(Base, BaseModelMixin):
    __tablename__ = "roles"

    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
from decimal import Decimal

from pydantic import BaseModel


class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    categoria: str | None = None
    precio: Decimal
    stock_actual: int = 0
    stock_minimo: int = 0


class ProductoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    precio: Decimal | None = None
    stock_minimo: int | None = None


class ProductoResponse(BaseModel):
    uuid: str
    nombre: str
    descripcion: str | None
    categoria: str | None
    precio: Decimal
    stock_actual: int
    stock_minimo: int
from sqlalchemy.orm import Mapped, mapped_column
from models.base import BaseModel


class Producto(BaseModel):

    __tablename__ = "productos"

    nombre: Mapped[str]

    precio: Mapped[float]

    stock: Mapped[int]
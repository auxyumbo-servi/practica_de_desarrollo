from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel


class Cliente(BaseModel):

    __tablename__ = "clientes"

    nombre: Mapped[str]

    ventas: Mapped[list["Venta"]] = relationship(
        back_populates="cliente"
    )
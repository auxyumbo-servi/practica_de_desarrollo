from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from models.base import BaseModel


class Venta(BaseModel):

    __tablename__ = "ventas"


    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id")
    )


    cliente: Mapped["Cliente"] = relationship(
        back_populates="ventas"
    )


    detalles: Mapped[list["DetalleVenta"]] = relationship(
        back_populates="venta",
        cascade="all, delete-orphan"
    )
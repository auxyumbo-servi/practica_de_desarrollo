from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from models.base import BaseModel


class DetalleVenta(BaseModel):

    __tablename__ = "detalle_ventas"


    venta_id: Mapped[int] = mapped_column(
        ForeignKey("ventas.id")
    )


    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id")
    )


    cantidad: Mapped[int]


    precio: Mapped[float]


    venta: Mapped["Venta"] = relationship(
        back_populates="detalles"
    )
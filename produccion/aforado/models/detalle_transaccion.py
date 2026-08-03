from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import ForeignKey

from models.base import BaseModel


class DetalleTransaccion(BaseModel):

    __tablename__ = "detalle_transacciones"


    transaccion_id: Mapped[int] = mapped_column(
        ForeignKey(
            "transacciones.id"
        )
    )


    recipiente_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recipientes.id"
        )
    )


    cantidad: Mapped[int]


    precio: Mapped[float]


    transaccion: Mapped["Transaccion"] = relationship(
        "Transaccion",
        back_populates="detalles"
    )
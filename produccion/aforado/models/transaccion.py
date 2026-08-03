from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

from sqlalchemy import ForeignKey

from models.base import BaseModel


class Transaccion(BaseModel):

    __tablename__ = "transacciones"


    usuario_id: Mapped[int] = mapped_column(
        ForeignKey(
            "usuarios.id"
        )
    )


    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="transacciones"
    )


    detalles: Mapped[list["DetalleTransaccion"]] = relationship(
        "DetalleTransaccion",
        back_populates="transaccion",
        cascade="all, delete-orphan"
    )
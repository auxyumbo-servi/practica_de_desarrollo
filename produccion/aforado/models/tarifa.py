from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.conexion import Base


if TYPE_CHECKING:
    from .registro_servicio import RegistroServicio
    from .tipo_servicio import TipoServicio


class Tarifa(Base):
    __tablename__ = "tarifas"

    id: Mapped[int] = mapped_column(primary_key=True)

    cliente_id: Mapped[int] = mapped_column(
        String(100),
        ForeignKey("clientes.id")
    )
    tipo_servicio_id: Mapped[int] = mapped_column(
        String(100),
        ForeignKey("tipos_servicio.id")
    )
    
    valor_unitario: Mapped[int] 

    registros: Mapped[list["RegistroServicio"]] = relationship(
        back_populates="tarifa"
    )

    tipo_servicio: Mapped["TipoServicio"] = relationship(
        back_populates="tarifas"
    )

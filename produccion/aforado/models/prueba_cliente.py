from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.conexion import Base


if TYPE_CHECKING:
    from .registro_servicio import RegistroServicio
    from .tarifa import Tarifa


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    contrato: Mapped[str]

    registros: Mapped[list["RegistroServicio"]] = relationship(
        back_populates="cliente"
    )

    tarifas: Mapped[list["Tarifa"]] = relationship(
        back_populates="cliente"
    )

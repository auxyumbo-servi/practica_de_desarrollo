from typing import TYPE_CHECKING

from sqlalchemy import  String, Integer, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from data.conexion import Base

if TYPE_CHECKING:
    from .registro_servicio import RegistroServicio

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id: Mapped[int] = mapped_column(primary_key=True)

    placa: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True
    )

    registros: Mapped[list["RegistroServicio"]] = relationship(
        back_populates="vehiculo"
    )



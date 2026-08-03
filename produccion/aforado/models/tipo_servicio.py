from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.cliente import Base

if TYPE_CHECKING:
    from .registro_servicio import RegistroServicio
    from .tarifa import Tarifa

class TipoServicio(Base):
    __tablename__ = "tipos_servicio"

    id: Mapped[int] = mapped_column(primary_key=True)

    tipo: Mapped[str] = mapped_column(
        String(10),
        unique=True
    )

    registros: Mapped[list["RegistroServicio"]] = relationship(
        back_populates="tipo_servicio"
    )

    tarifas: Mapped[list["Tarifa"]] = relationship(
        back_populates="tipo_servicio"
    )
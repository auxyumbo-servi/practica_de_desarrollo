from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.cliente import Base

if TYPE_CHECKING:
    from .registro_servicio import RegistroServicio

class TipoServicio(Base):
    __tablename__ = "tipos_servicio"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )

    registros: Mapped[list["RegistroServicio"]] = relationship(
        back_populates="tipo_servicio"
    )
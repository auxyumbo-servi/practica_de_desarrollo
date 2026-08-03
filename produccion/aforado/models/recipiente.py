from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.cliente import Base

if TYPE_CHECKING:
    from .registro_servicio import RegistroServicio
    
class Recipiente(Base):
    __tablename__ = "recipientes"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(String(50))

    equivalencia: Mapped[float] = mapped_column(Numeric(10,2), nullable=True)

    registros: Mapped[list["RegistroServicio"]] = relationship(
        back_populates="recipiente"
    )
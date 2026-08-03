from typing import TYPE_CHECKING

from sqlalchemy import  String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship

from data.conexion import Base

if TYPE_CHECKING:
    from .registro_servicio import RegistroServicio
    from .cliente import Cliente


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True)

    nombre: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    cliente_id: Mapped[int] = mapped_column(
            ForeignKey("clientes.id")
        )
    
    cliente: Mapped["Cliente"] = relationship()

    registros: Mapped[list["RegistroServicio"]] = relationship(
        back_populates="empresa"
    )


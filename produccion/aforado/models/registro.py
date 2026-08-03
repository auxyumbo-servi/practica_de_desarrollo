from typing import TYPE_CHECKING

from datetime import date
from sqlalchemy import ForeignKey, String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.cliente import Base

if TYPE_CHECKING:
    from models.cliente import Cliente
    from models.empresa import Empresa
    from models.recipiente import Recipiente
    from models.tipo_servicio import TipoServicio
    from models.vehiculo import Vehiculo
    from .tarifa import Tarifa
    from .tipo_servicio import TipoServicio


class RegistroServicio(Base):
    __tablename__ = "registros"

    id: Mapped[int] = mapped_column(primary_key=True)

    fecha: Mapped[date] = mapped_column(Date)

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id")
    )

    vehiculo_id: Mapped[int | None] = mapped_column(
        ForeignKey("vehiculos.id")
    )

    recipiente_id: Mapped[int] = mapped_column(
        ForeignKey("recipientes.id")
    )

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id")
    )

    tipo_servicio_id: Mapped[int | None] = mapped_column(
        ForeignKey("tipos_servicio.id")
    )

    tarifa_id: Mapped[int | None] = mapped_column(
        ForeignKey("tarifas.id")
    )

    aforo: Mapped[float]

    cantidad: Mapped[int]

    subtotal: Mapped[float]

    valor: Mapped[float]

    facturable: Mapped[bool] = mapped_column(default=True)

    minicargador: Mapped[bool | None]= mapped_column(default=False)

    observacion: Mapped[str | None] = mapped_column(Text)

    cliente: Mapped["Cliente"] = relationship(back_populates="registros")
    vehiculo: Mapped["Vehiculo | None"] = relationship(back_populates="registros")
    recipiente: Mapped["Recipiente"] = relationship(back_populates="registros")
    empresa: Mapped["Empresa"] = relationship(back_populates="registros")
    tipo_servicio: Mapped["TipoServicio | None"] = relationship(back_populates="registros")
    tarifa: Mapped["Tarifa | None"] = relationship(back_populates="registros")
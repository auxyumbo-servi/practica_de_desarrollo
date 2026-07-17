from sqlalchemy import Column, Integer, String
from .conexion import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)

    nombre = Column(
        String(100),
        nullable=False
    )

    apellido = Column(
        String(100)
    )

    documento = Column(
        String(50),
        unique=True
    )

    telefono = Column(
        String(50)
    )

    correo = Column(
        String(100)
    )
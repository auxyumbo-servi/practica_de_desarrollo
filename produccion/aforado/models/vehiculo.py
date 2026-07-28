from sqlalchemy import Column, Integer, String
from data.conexion import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String)
    valor = Column(Integer)
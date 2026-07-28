from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data.conexion import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    contrato = Column(String)
    empresa_id = Column(ForeignKey("empresas.id"))

empresa = relationship("Empresa")
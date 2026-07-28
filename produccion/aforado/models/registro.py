from sqlalchemy import Column, Integer, String, Date , ForeignKey
from sqlalchemy.orm import relationship
from data.conexion import Base

class Encabezado(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    cliente_id = Column(ForeignKey("clientes.id"))
    aforo = Column(String)
    
empresa = relationship("Cliente")

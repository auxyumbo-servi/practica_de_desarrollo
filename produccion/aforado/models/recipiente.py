from sqlalchemy import Column, Integer, String, Float
from data.conexion import Base

class Recipiente(Base):
    __tablename__ = "recipientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    equivalencia = Column(Float)

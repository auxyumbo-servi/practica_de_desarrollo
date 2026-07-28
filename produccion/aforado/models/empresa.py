from sqlalchemy import Column, Integer, String
from data.conexion import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

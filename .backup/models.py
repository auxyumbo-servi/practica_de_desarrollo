from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

Base = None
#==== Datos Basicos de Formulario ====#

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    contrato = Column(String)

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)

class Recipiente(Base):
    __tablename__ = "recipientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    equivalencia = Column(Float)

#==== Datos Especiales de Formulario ====#

class Tarifa(Base):
    __tablename__ = "tarifas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    valor = Column(Integer)

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True)
    placa = Column(String)
    tipo = Column(String)

#==== Tabla de Produccion ====#

class Produccion(Base):
    __tablename__ = "produccion"

    id = Column(Integer, primary_key=True)

    fecha = Column(Date)

    cliente_id = Column(ForeignKey("clientes.id"))
    empresa_id = Column(ForeignKey("empresas.id"))
    vehiculo_id = Column(ForeignKey("vehiculos.id"))
    tarifa_id = Column(ForeignKey("tarifas.id"))
    recipiente_id = Column(ForeignKey("recipientes.id"))

    cliente = relationship("Cliente")
    empresa = relationship("Empresa")
    vehiculo = relationship("Vehiculo")
    tarifa = relationship("Tarifa")
    recipiente = relationship("Recipiente")

#==== Detalles de Aforado ====#

class Detalle_produccion(Base):
    __tablename__ = "detalle_produccion"

    id = Column(Integer, primary_key=True)

    fecha = Column(Date)

    clienteId = Column(ForeignKey("clientes.id"))
    empresaId = Column(ForeignKey("empresas.id"))
    recipienteId = Column(ForeignKey("recipientes.id"))

    cantidad = Column(Integer)

    observacion = Column(String)
    cliente = relationship("Cliente")
    empresa = relationship("Empresa")
    recipiente = relationship("Recipiente")
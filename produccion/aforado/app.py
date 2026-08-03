from nicegui import ui

from data.conexion import engine
from models.cliente import Base
from models.empresa import Base
from models.recipiente import Base
from models.registro_servicio import Base
from models.tipo_servicio import Base
from models.vehiculo import Base

# Crear tablas
Base.metadata.create_all(engine)

from pages import inicio
from pages import crear_cliente
from pages import test

ui.run()
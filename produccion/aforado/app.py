from nicegui import ui
from database import SessionLocal
from models import Cliente, Detalle_produccion

def guardar_registro():


    session = SessionLocal()
    
    registro = Detalle_produccion(
        cantidad=input_cantidad.value,
    )

    session.add(registro)
    session.commit()

    session.close()

    input_cantidad.value = ""
    
with ui.card():
    ui.label("Registro...")

    input_cantidad =ui.input(label="cantidad")
    ui.button(
        "guardar",
        on_click=guardar_registro
        )


def guardar_cliente():

    session = SessionLocal()

    cliente = Cliente(
        nombre=input_nombre.value,
        contrato=input_contrato.value
    )

    session.add(cliente)
    session.commit()

    session.close()

    ui.notify("Cliente guardado correctamente")

    input_nombre.value = ""
    input_contrato.value = ""

    with ui.card():

        ui.label("Nuevo Cliente")

        input_nombre = ui.input(
            label="Nombre"
        )

        input_contrato = ui.input(
            label="Contrato"
        )

        ui.button(
            "Guardar",
            on_click=guardar_cliente
        )

ui.run()
from nicegui import ui
from produccion.backup.database.database import SessionLocal
from models import Cliente


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

#guardar
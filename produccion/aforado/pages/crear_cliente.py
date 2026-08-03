from nicegui import ui

from data.conexion import SessionLocal
from models.cliente import Cliente


@ui.page("/crear")
def crear_cliente():

    params = ui.context.client.request.query_params

    documento = ui.input(
        "Documento",
        value=params.get("doc", ""),
    )

    nombre = ui.input("Nombre")
    telefono = ui.input("Teléfono")
    correo = ui.input("Correo")

    def guardar():

        with SessionLocal() as db:

            cliente = Cliente(
                documento=documento.value,
                nombre=nombre.value,
                telefono=telefono.value,
                correo=correo.value,
            )

            db.add(cliente)
            db.commit()

        ui.notify("Cliente creado")

        ui.navigate.to(f"/?doc={documento.value}")

    ui.button(
        "Guardar",
        on_click=guardar,
    )
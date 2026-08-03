from nicegui import ui

from data.conexion import SessionLocal
from models.cliente import Cliente


@ui.page("/test")
def inicio():

    documento = ui.input("Documento")

    def buscar():

        with SessionLocal() as db:

            cliente = (
                db.query(Cliente)
                .filter(Cliente.documento == documento.value)
                .first()
            )

            if cliente:
                ui.notify(f"Bienvenido {cliente.nombre}")
            else:
                ui.navigate.to(f"/crear?doc={documento.value}")

    ui.label("Formulario principal")

    ui.button(
        "Buscar cliente",
        on_click=buscar,
    )

    ui.input("Producto")
    ui.input("Cantidad")     
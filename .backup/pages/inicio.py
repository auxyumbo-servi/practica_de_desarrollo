from nicegui import ui
from database.database import SessionLocal
from models import Detalle_produccion


@ui.page('/')
def guardar_registro():


    session = SessionLocal()
    
    registro = Detalle_produccion(
        cantidad=input_cantidad.value,
    )

    session.add(registro)
    session.commit()

    session.close()

    input_cantidad.value = ""
    
with ui.row():

        ui.button(
            'Clientes',
            on_click=lambda: ui.navigate.to('/clientes')
        )

        ui.button(
            'Productos',
            on_click=lambda: ui.navigate.to('/productos')
        )

        ui.button(
            'Ventas',
            on_click=lambda: ui.navigate.to('/ventas')
        )
        with ui.card():
            ui.label("Registro...")

            input_cantidad =ui.input(label="cantidad")
            ui.button(
                "guardar",
                on_click=guardar_registro
                )

            ui.label('Registro').classes('text-3xl')
ui.run()
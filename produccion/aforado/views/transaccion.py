from nicegui import ui

from controllers.transaccion_controller import TransaccionController


controller = TransaccionController()


@ui.page("/")
def transacciones():

    recipientes = []

    usuario = ui.number(
        label="Usuario"
    )

    recipiente = ui.number(
        label="Recipiente"
    )

    cantidad = ui.number(
        label="Cantidad"
    )


    tabla = ui.table(
        columns=[
            {
                "name": "recipiente",
                "label": "Recipiente",
                "field": "recipiente"
            },
            {
                "name": "cantidad",
                "label": "Cantidad",
                "field": "cantidad"
            }
        ],
        rows=[]
    )


    def agregar():

        if not recipiente.value:
            ui.notify(
                "Seleccione un recipiente"
            )
            return


        if not cantidad.value:
            ui.notify(
                "Ingrese una cantidad"
            )
            return


        item = {

            "recipiente_id": int(recipiente.value),

            "cantidad": int(cantidad.value)

        }


        recipientes.append(item)


        tabla.rows = recipientes
        tabla.update()


        print(
            "LISTA ACTUAL:",
            recipientes
        )


        # limpiar solo los campos de entrada
        recipiente.value = None
        cantidad.value = None



    def guardar():

        if not usuario.value:

            ui.notify(
                "Seleccione un usuario"
            )

            return


        detalles = recipientes.copy()


        # Caso donde no se usó el botón agregar
        # toma directamente el recipiente actual

        if not detalles:


            if not recipiente.value:

                ui.notify(
                    "Seleccione un recipiente"
                )

                return


            if not cantidad.value:

                ui.notify(
                    "Ingrese una cantidad"
                )

                return


            detalles.append({

                "recipiente_id": int(recipiente.value),

                "cantidad": int(cantidad.value)

            })


        print(
            "DETALLES ENVIADOS:",
            detalles
        )


        try:

            resultado = controller.guardar(

                int(usuario.value),

                detalles

            )


            ui.notify(
                f"Transacción creada: {resultado.id}"
            )


            # limpiar detalles acumulados

            recipientes.clear()


            tabla.rows = []
            tabla.update()


            # limpiar campos

            usuario.value = None
            recipiente.value = None
            cantidad.value = None


        except Exception as e:

            ui.notify(
                f"Error: {e}"
            )



    ui.button(
        "Agregar recipiente",
        on_click=agregar
    )


    ui.button(
        "Guardar",
        on_click=guardar
    )
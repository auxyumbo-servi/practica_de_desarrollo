from nicegui import ui

from controllers.venta_controller import VentaController



controller = VentaController()



productos = []



@ui.page("/")
def ventas():


    ui.label(
        "Nueva Venta"
    )


    cliente = ui.number(
        label="Cliente ID"
    )



    producto = ui.number(
        label="Producto ID"
    )


    cantidad = ui.number(
        label="Cantidad"
    )



    tabla = ui.table(
        columns=[
            {
                "name":"producto",
                "label":"Producto",
                "field":"producto"
            },
            {
                "name":"cantidad",
                "label":"Cantidad",
                "field":"cantidad"
            }
        ],
        rows=[]
    )



    def agregar_producto():

        item = {

            "producto_id":
            producto.value,

            "cantidad":
            cantidad.value

        }


        productos.append(item)


        tabla.rows = productos

        tabla.update()



    def guardar():

        venta = controller.guardar(

            cliente.value,

            productos

        )


        ui.notify(
            f"Venta creada {venta.id}"
        )



    ui.button(
        "Agregar producto",
        on_click=agregar_producto
    )


    ui.button(
        "Guardar venta",
        on_click=guardar
    )
from nicegui import ui


@ui.page
def produccion():

    with ui.card().classes(
            'widt: 50%;'
            'margin: auto;'
            ):
        rows = [

        ]

        tabla = ui.table(
            columns=[
                {'name': 'recipiente', 'label': 'Recipiente', 'field': 'recipiente'},
                {'name': 'cantidad', 'label': 'Cantidad', 'field': 'cantidad'},
                {'name': 'valor', 'label': 'Valor', 'field': 'valor'},
                {'name': 'subtotal', 'label': 'Subtotal', 'field': 'subtotal'},
            ],
            rows=rows,
        )


        
    with ui.row():
        recipiente = ui.select(
            ['55GL', '1000L', '2YD', '3YD'],
            label='Recipiente'
        )

        cantidad = ui.number('Cantidad', value=1)

    def agregar():
        subtotal = cantidad.value * 25000

        rows.append({
            'recipiente': recipiente.value,
            'cantidad': cantidad.value,
            'valor': 25000,
            'subtotal': subtotal,
        })

        tabla.update()

    ui.button('Agregar', on_click=agregar)

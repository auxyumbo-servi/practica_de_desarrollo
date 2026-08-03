from nicegui import ui


@ui.page('/produccion')
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


    with ui.footer().classes('bg-yellow-400 text-black justify-around'):
        ui.button('Crear cliente', on_click=lambda: ui.navigate.to('/Newcliente')).props('bg-yellow-450 text-color=black')
        ui.button('Crear Empresa', on_click=lambda: ui.navigate.to('/NewEmpresa')) .props('bg-yellow-450 text-color=black')
        ui.button('Produccion', on_click=lambda: ui.navigate.to('/produccion')) .props('bg-yellow-450 text-color=black')
        ui.button('inicio', on_click=lambda: ui.navigate.to('/')).props('bg-yellow-450 text-color=black')
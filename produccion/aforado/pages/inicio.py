from nicegui import ui


with ui.header().classes('bg-yellow-400 text-black w-full'):
        fecha = ui.date_input(label='Fecha' )
        tipo_servicio = ui.checkbox('Servicios S&S')

with ui.column().style(
    'width: 50%; '
    'max-width: 1400px; '
    'margin: auto;'
):

    with ui.card().classes(
        'widt: 50%;'
        'margin: auto;'
        ):

        with ui.row().classes('justify-center;'
                            'w-full'):
            
            cliente = ui.select(
                options=[],
                label='Cliente',
                with_input=True
            )

            empresa = ui.select(
                options=[],
                label='Empresa',
                with_input=True
            )

        with ui.row().classes('w-full;'
                            'wight:50%'):

            servicio = ui.select(
                [],
                with_input=True
            )

            tipo = ui.select(
                [],
                with_input=True
            )
            guardar = ui.button('GUARDAR').classes('justify-center;').props('bg-yellow-450 text-color=black')



with ui.footer().classes('bg-yellow-400 text-black justify-around'):
    ui.button('atras', on_click=lambda: ui.navigate.to('/')).props('bg-yellow-450 text-color=black')
    ui.button('Crear cliente', on_click=lambda: ui.navigate.to('/Newcliente')).props('bg-yellow-450 text-color=black')
    ui.button('Crear Empresa', on_click=lambda: ui.navigate.to('/NewEmpresa')) .props('bg-yellow-450 text-color=black')
    ui.button('Produccion', on_click=lambda: ui.navigate.to('/produccion')) .props('bg-yellow-450 text-color=black')


ui.run()
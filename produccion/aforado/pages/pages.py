from nicegui import ui

ui.colors(
    primary="#FBFF00",
    secondary="#FC0000",
    accent="#1150FD",
    positive='#2E8B57',
)

# -------------------------
# Encabezado
# -------------------------

with ui.header(elevated=True).classes('items-center justify-between'):

    ui.label('📋 Sistema de Registro').classes('text-h5')

    with ui.row().classes('items-center'):
        ui.label('Fecha:')
        ui.input(value='24/07/2026').props('readonly outlined dense').style('width:140px')
        ui.button('Cambiar', icon='event')

        ui.separator().props('vertical')

        ui.icon('person')
        ui.label('Administrador')

        ui.button(icon='logout')


# -------------------------
# Menú lateral
# -------------------------

with ui.left_drawer(top_corner=True, bottom_corner=True).classes('bg-blue-900 text-white'):

    ui.label('MENÚ').classes('text-h6 q-pa-md')

    ui.separator()

    ui.button('🏠 Inicio').props('flat').classes('w-full justify-start')
    ui.button('📝 Nuevo Registro').props('flat').classes('w-full justify-start')
    ui.button('👥 Clientes').props('flat').classes('w-full justify-start')
    ui.button('📦 Productos').props('flat').classes('w-full justify-start')
    ui.button('📊 Consultas').props('flat').classes('w-full justify-start')
    ui.button('📈 Reportes').props('flat').classes('w-full justify-start')
    ui.button('⚙ Configuración').props('flat').classes('w-full justify-start')


# -------------------------
# Contenido principal
# -------------------------

with ui.row().classes('w-full no-wrap'):

    # ------------------------
    # Formulario
    # ------------------------

    with ui.card().classes('w-3/4 p-6'):

        ui.label('REGISTRO DIARIO').classes('text-h5')

        ui.separator()

        ui.space()

        ui.input(
            label='Cliente',
            placeholder='Buscar cliente...'
        ).props('outlined clearable')

        ui.space()

        ui.label('Productos').classes('text-subtitle1')

        columns = [
            {'name':'producto','label':'Producto','field':'producto'},
            {'name':'cantidad','label':'Cantidad','field':'cantidad'},
            {'name':'accion','label':'Acción','field':'accion'},
        ]

        rows = [
            {
                'producto':'Coca Cola',
                'cantidad':2,
                'accion':'🗑'
            },
            {
                'producto':'Pan Tajado',
                'cantidad':5,
                'accion':'🗑'
            },
        ]

        ui.table(
            columns=columns,
            rows=rows
        ).classes('w-full')

        ui.space()

        with ui.row():

            ui.input(
                label='Producto'
            ).props('outlined')

            ui.number(
                label='Cantidad',
                value=1
            ).props('outlined')

            ui.button(
                'Agregar',
                icon='add',
                color='positive'
            )

        ui.space()

        ui.textarea(
            label='Observaciones'
        ).props('outlined').classes('w-full')

        ui.space()

        with ui.row():

            ui.button(
                'Guardar',
                icon='save',
                color='positive'
            )

            ui.button(
                'Limpiar',
                icon='cleaning_services'
            )

            ui.button(
                'Nuevo',
                icon='note_add'
            )

    # ------------------------
    # Panel derecho
    # ------------------------

    with ui.card().classes('w-1/4 p-6'):

        ui.label('Resumen').classes('text-h6')

        ui.separator()

        ui.label('Cliente')
        ui.label('Juan Pérez').classes('text-bold')

        ui.separator()

        ui.label('Productos')
        ui.label('2')

        ui.separator()

        ui.label('Cantidad Total')
        ui.label('7')

        ui.separator()

        ui.label('Último Registro')
        ui.label('09:25 AM')


ui.run(
    title='Sistema de Registro',
    reload=False
)
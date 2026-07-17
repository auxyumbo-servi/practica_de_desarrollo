from textual.app import ComposeResult
from textual.screen import Screen

from textual.widgets import (
    Input,
    Label,
    ListView,
    ListItem,
    Static,
    Button
)

from textual.containers import Horizontal

from database.conexion import SessionLocal
from database.modelos import Usuario


class BusquedaUsuario(Screen):

    def __init__(self):
        super().__init__()
        self.usuario_actual = None

    def compose(self) -> ComposeResult:

        yield Label(
            "BUSQUEDA DE USUARIOS"
        )

        yield Input(
            placeholder="Buscar nombre o documento...",
            id="buscar"
        )

        with Horizontal():

            yield ListView(
                id="resultados"
            )

            yield Static(
                "Seleccione un usuario",
                id="detalle"
            )

            yield Button(
                "Editar",
                id="editar"
            )


    def on_input_changed(self, event):

        if event.input.id != "buscar":
            return


        texto = event.value


        lista = self.query_one(
            "#resultados"
        )


        lista.clear()


        if not texto:
            return


        db = SessionLocal()


        usuarios = db.query(Usuario).filter(
            (Usuario.nombre.like(f"%{texto}%")) |
            (Usuario.documento.like(f"%{texto}%"))
        ).limit(30).all()


        db.close()


        for usuario in usuarios:

            item = ListItem(
                Label(
                    f"{usuario.nombre} {usuario.apellido}"
                )
            )

            item.usuario_id = usuario.id

            lista.append(item)



    def on_list_view_selected(
            self,
            event: ListView.Selected
    ):

        item = event.item


        usuario_id = item.usuario_id


        db = SessionLocal()


        usuario = db.query(
            Usuario
        ).filter(
            Usuario.id == usuario_id
        ).first()


        db.close()


        detalle = f"""
DATOS DEL USUARIO

Nombre:
{usuario.nombre} {usuario.apellido}

Documento:
{usuario.documento}

Telefono:
{usuario.telefono}

Correo:
{usuario.correo}

ID:
{usuario.id}
"""


        self.query_one(
            "#detalle"
        ).update(detalle)
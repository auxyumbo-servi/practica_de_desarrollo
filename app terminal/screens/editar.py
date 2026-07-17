from textual.app import ComposeResult
from textual.screen import Screen

from textual.widgets import (
    Input,
    Button,
    Label
)

from database.conexion import SessionLocal
from database.modelos import Usuario


class EditarUsuario(Screen):

    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id


    def compose(self) -> ComposeResult:

        db = SessionLocal()

        usuario = db.query(
            Usuario
        ).filter(
            Usuario.id == self.usuario_id
        ).first()

        db.close()


        yield Label(
            "EDITAR USUARIO"
        )


        yield Input(
            value=usuario.nombre,
            id="nombre"
        )


        yield Input(
            value=usuario.apellido,
            id="apellido"
        )


        yield Input(
            value=usuario.documento,
            id="documento"
        )


        yield Input(
            value=usuario.telefono,
            id="telefono"
        )


        yield Input(
            value=usuario.correo,
            id="correo"
        )


        yield Button(
            "Guardar cambios",
            id="guardar"
        )


        yield Label(
            "",
            id="mensaje"
        )



    def on_button_pressed(self,event):

        if event.button.id == "guardar":


            db = SessionLocal()


            usuario = db.query(
                Usuario
            ).filter(
                Usuario.id == self.usuario_id
            ).first()



            usuario.nombre = self.query_one(
                "#nombre"
            ).value


            usuario.apellido = self.query_one(
                "#apellido"
            ).value


            usuario.documento = self.query_one(
                "#documento"
            ).value


            usuario.telefono = self.query_one(
                "#telefono"
            ).value


            usuario.correo = self.query_one(
                "#correo"
            ).value



            db.commit()
            db.close()


            self.query_one(
                "#mensaje"
            ).update(
                "Cambios guardados"
            )
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Input,
    Button,
    Label
)

from database.conexion import SessionLocal
from database.modelos import Usuario


class FormularioUsuario(Screen):

    def compose(self) -> ComposeResult:

        yield Label("REGISTRO DE USUARIO")

        yield Input(
            placeholder="Nombre",
            id="nombre"
        )

        yield Input(
            placeholder="Apellido",
            id="apellido"
        )

        yield Input(
            placeholder="Documento",
            id="documento"
        )

        yield Input(
            placeholder="Telefono",
            id="telefono"
        )

        yield Input(
            placeholder="Correo",
            id="correo"
        )

        yield Button(
            "Guardar",
            id="guardar"
        )

        yield Label(
            "",
            id="mensaje"
        )


    def on_button_pressed(self, event):

        if event.button.id == "guardar":

            nombre = self.query_one("#nombre").value
            apellido = self.query_one("#apellido").value
            documento = self.query_one("#documento").value
            telefono = self.query_one("#telefono").value
            correo = self.query_one("#correo").value


            if not nombre or not documento:

                self.query_one(
                    "#mensaje"
                ).update(
                    "Nombre y documento son obligatorios"
                )

                return


            db = SessionLocal()


            usuario = Usuario(
                nombre=nombre,
                apellido=apellido,
                documento=documento,
                telefono=telefono,
                correo=correo
            )


            db.add(usuario)
            db.commit()
            db.close()


            self.query_one(
                "#mensaje"
            ).update(
                "Usuario guardado correctamente"
            )
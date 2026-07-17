from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label
from database.conexion import Base, engine
from screens.formulario import FormularioUsuario
from screens.busqueda import BusquedaUsuario

Base.metadata.create_all(engine)


class SistemaUsuarios(App):

    CSS_PATH = "styles.tcss"




class SistemaUsuarios(App):

    def compose(self) -> ComposeResult:

        yield Header()

        yield Label(
            "SISTEMA DE USUARIOS"
        )

        yield Button(
            "Nuevo Usuario",
            id="nuevo"
        )
        yield Button(
        "Buscar Usuario",
        id="buscar"
        )

        yield Footer()


    def on_button_pressed(self, event):

        if event.button.id == "nuevo":

            self.push_screen(
            FormularioUsuario()
        )


        if event.button.id == "buscar":

            self.push_screen(
            BusquedaUsuario()
        )


if __name__ == "__main__":

    app = SistemaUsuarios()

    app.run()
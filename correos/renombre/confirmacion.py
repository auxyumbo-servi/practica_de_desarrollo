from renombre.lista import *
from renombre.renombrar import *

def accion():
    listar()

    if input("¿Desea renombrar los archivos PDF? (s/n): ").strip().lower() == "s":
        renombrar()
    else:
        print("Proceso de renombrado cancelado.")

    
if __name__ == "__main__":
    pass
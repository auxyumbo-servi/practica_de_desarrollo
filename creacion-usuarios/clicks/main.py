import cargar_produccion
import capturar_clicks
import eliminacion_usuario
import crear_usuario 

while True:
    print("\n===== MENÚ =====")
    print("1. Cargar produccion")
    print("2. Captura de clicks para mapeo")
    print("3. crear usuarios")
    print("4. eliminar usuarios")
    print("5. test")
    print("0. Salir\n")

    opcion = input("Seleccione una opción: ")

    


    match opcion:
        case "1":
            cargar_produccion.iniciar()

        case "2":
            capturar_clicks.iniciar()

        case "3":
            crear_usuario.iniciar()

        case "4":
            eliminacion_usuario.iniciar()
            
        case "5":
            pass

        case "0":
            print("Hasta luego.")
            break

        case _:
            print("Opción inválida.")
        
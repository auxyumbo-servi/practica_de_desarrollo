import pyautogui
import keyboard
import time

cantidad_clicks = 1


clicks= (
    (906, 287),
    (918, 332),
    (791, 368)
    )



def iniciar():
    def ejecutar_accion(accion):
        tipo = accion[0]

        if tipo == "click":
            x, y = accion[1]
            pyautogui.click(x, y)

        elif tipo == "hotkey":
            pyautogui.hotkey(*accion[1])

        time.sleep(0.5)


    def secuencia():
        cancelar = False

        while not cancelar:

            acciones = [          # Registro

                ("click", clicks[0]),          # Registro
                ("click", clicks[1]),          # Registro
                ("click", clicks[2]),          # Registro
                ("hotkey", ("esc",)),
            ]

            for accion in acciones:
                if keyboard.is_pressed("shift"):
                    return False

                ejecutar_accion(accion)

        return True


    def cargue():
        for i in range(cantidad_clicks):
            print(f"Iteración {i + 1}/{cantidad_clicks}")

            if not secuencia():
                print("Proceso detenido.")
                return

        print("Proceso terminado.")


    def detener():
        global cancelar
        cancelar = True
        print("\rCancelando proceso...",end="", flush=True)


    print("=======================================")
    print("Ctrl + Enter  -> Iniciar")
    print("Shift         -> Detener")
    print("0           -> Salir")
    print("=======================================")
    
    keyboard.add_hotkey("ctrl+enter", cargue)
    keyboard.add_hotkey("shift", detener)

    keyboard.wait("0")
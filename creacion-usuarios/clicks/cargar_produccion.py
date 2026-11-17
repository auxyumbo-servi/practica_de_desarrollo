import pyautogui
import keyboard
import time
from confi_fecha import  fecha_anterior

fecha = fecha_anterior()
mes = str(fecha.mes)
completa = str(fecha.dia) + str(fecha.mes) +str(fecha.año)

cantidad_clicks = 1

click_aforo = (1815,120)
click_metros = (1722, 120)

consecutivo = (467,282)
metros = (467,762)

click_crear = (397, 247)
click_regresar = (1348, 250)

# el dato superior 

inicio = [
    (1585, 455)
    ]

# el dato inferior 

fin = [
    (1593, 545)
    ]
    
x = fin[0][0]
y1 = fin[0][1]
y2 = inicio[0][1]

def iniciar():
    def ejecutar_accion(accion):
        tipo = accion[0]

        if tipo == "click":
            x, y = accion[1]
            pyautogui.click(x, y)

        elif tipo == "hotkey":
            pyautogui.hotkey(*accion[1])

        elif tipo == "write":
            pyautogui.write(accion[1])

        time.sleep(0.5)


    def secuencia():
        for y in range(y1, y2, -20):

            acciones = [
                ("click", (int(x),int(y))),          # Registro

                ("hotkey", ("alt", "tab")),
                ("click", click_aforo),
                ("click", click_aforo),
                ("hotkey", ("ctrl", "c")),

                ("click", consecutivo),
                ("write", mes + "-"),
                ("hotkey", ("ctrl", "v")),

                ("hotkey", ("tab",)),
                ("write", completa),

                ("hotkey", ("alt", "tab")),
                ("click", click_metros),
                ("click", click_metros),
                ("hotkey", ("ctrl", "c")),

                ("click", metros),
                ("hotkey", ("ctrl", "v")),
                
                ("click", click_crear),
                ("click", click_regresar),
                ("click", click_regresar),

                ("hotkey", ("alt", "tab")),
                ("hotkey", ("up",)),
                ("hotkey", ("alt", "tab")),
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
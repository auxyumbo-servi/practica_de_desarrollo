import pyautogui
import keyboard
import time

cantidad_clicks = 20

eliminacion_centrada = (
    (807, 295),
    (815, 343),
    (803, 382)  )

eliminacion_derecha = (
    (1317, 644), 
    (1351, 280), 
    (1335, 280), 
    (1342, 280), 
    (856, 539), 
    (1127, 252),
)

eliminacion_usuario = (

    (1322, 481), 
    # (1340, 481), 
    (850, 537), 
)
ingreso_registro = (1301, 483) 
checkbox_permanentes = (773, 353)  
clicks_eliminacion = (ingreso_registro, checkbox_permanentes) + eliminacion_derecha + eliminacion_centrada + (checkbox_permanentes,) + eliminacion_usuario + (checkbox_permanentes,)

def iniciar(): 

    def secuencia():
        for click in clicks_eliminacion:
            if keyboard.is_pressed("shift"):
                return False

            pyautogui.click(click)
            time.sleep(0.2)
            pyautogui.hotkey("esc")

        return True


    def cargue():
        for i in range(cantidad_clicks):
            print(f"Iteración {i+1}/{cantidad_clicks}")

            if not secuencia():
                print("Proceso detenido.")
                return

        print("Proceso terminado.")

    print("Listo. Ctrl+Enter ejecuta | mantener 'shift' presionado sale")



    keyboard.add_hotkey("ctrl+enter",cargue)
    keyboard.wait("shift")



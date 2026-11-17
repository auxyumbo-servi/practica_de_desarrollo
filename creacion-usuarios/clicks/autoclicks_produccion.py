import pyautogui
import keyboard  # pip install keyboard
import time

# coordenadas de ejemplo
click1 = (1543, 291)
click2 = (392, 280)
click3 = (389, 301)
click4 = (342, 385)
click5 = (1462, 292)
click6 = (1462, 292)
click7 = (351, 764)
click8 = (271, 249)
click9 = (856, 245)

# 1. click en campo origen
def secuencia():

    pyautogui.click(click1)
    time.sleep(0.7)

    pyautogui.click(click1)
    time.sleep(1.5)

    # 2. copiar (Ctrl + C)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)

    # 3. click en campo destino
    pyautogui.click(click2)
    time.sleep(0.3)

    pyautogui.write("5-")

    # 4. pegar (Ctrl + V)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)

    # 5. click final (por ejemplo botón)
    pyautogui.click(click3)

    # 1. click en campo origen
    pyautogui.click(click4)
    time.sleep(0.3)

    # 5. click final (por ejemplo botón)
    pyautogui.click(click5)
    time.sleep(1)

    # 1. click en campo origen
    pyautogui.click(click6)
    time.sleep(0.3)

    # 2. copiar (Ctrl + C)
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)

    # 3. click en campo destino
    pyautogui.click(click7)
    time.sleep(0.3)

    # 4. pegar (Ctrl + V)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)

    # 5. click final (por ejemplo botón)
    pyautogui.click(click8)
    time.sleep(1)

    pyautogui.click(click9)
    time.sleep(0.5)

    pyautogui.hotkey("alt", "tab")
    time.sleep(0.3)

    pyautogui.hotkey("up")
    time.sleep(0.3)

    pyautogui.hotkey("left")

    print("Listo", end="\r")

print("Listo. Ctrl+Shift+l ejecuta | q sale")

keyboard.add_hotkey("ctrl+enter", secuencia)

keyboard.wait("q")
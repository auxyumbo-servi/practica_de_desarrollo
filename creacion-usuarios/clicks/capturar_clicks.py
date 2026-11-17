from pynput import mouse

coordenadas = []

def iniciar():
    print("Haz click en las posiciones que quieres guardar.")
    print("Presiona CTRL + C para terminar.\n")

    def on_click(x, y, button, pressed):
        if pressed:
            coordenadas.append((x, y))
            print(f"Guardado: X={x}, Y={y}")

    listener = mouse.Listener(on_click=on_click)

    try:
        listener.start()
        listener.join()   # Espera hasta que el listener termine
    except KeyboardInterrupt:
        listener.stop()
        print("\nCoordenadas guardadas:")
        for x, y in coordenadas:
            print(f"({x}, {y})")
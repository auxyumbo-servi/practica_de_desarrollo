
from config import MODO_ENVIO

from modules.excel_reader import leer_excel
from modules.data_processor import procesar_datos
from modules.email_builder import construir_correo
from modules.outlook_sender import OutlookSender
from modules.logger import configurar_logger
from renombre.confirmacion import accion


def main():
    accion()

    logger = configurar_logger()

    print("=" * 45)
    print("SISTEMA DE FACTURACIÓN AUTOMÁTICA")
    print("=" * 45)

    try:

        # 1. Leer Excel
        print("\n[1/4] Leyendo Excel...")

        df = leer_excel()

        # 2. Procesar información
        print("[2/4] Procesando información...")

        registros = procesar_datos(df)

        print(f"Registros válidos: {len(registros)}")

        # 3. Conectar Outlook
        print("[3/4] Conectando con Outlook...")

        outlook = OutlookSender()

        # 4. Generar y gestionar correos
        print("[4/4] Gestionando correos...")

        enviados = 0
        errores = 0

        for datos in registros:

            try:

                mensaje = construir_correo(datos)

                correo = outlook.enviar(
                    datos,
                    mensaje
                )

                resultado = outlook.gestionar(
                    correo,
                    MODO_ENVIO
                )

                enviados += 1

                logger.info(
                    "%s | %s | %s",
                    resultado,
                    datos["nombre"],
                    datos["correo"]
                )

                print(
                    f"[OK] {datos['nombre']} - {resultado}"
                )

            except Exception as error:

                errores += 1

                logger.exception(
                    "Error fila %s | %s",
                    datos["fila_excel"],
                    datos["nombre"]
                )

                print(
                    f"[ERROR] Fila {datos['fila_excel']}: {error}"
                )

        # Resumen final
        print("\n" + "=" * 45)
        print("RESUMEN DEL PROCESO")
        print("=" * 45)

        print(f"Registros válidos: {len(registros)}")
        print(f"Correos gestionados: {enviados}")
        print(f"Errores: {errores}")
        print(f"Modo utilizado: {MODO_ENVIO}")

        logger.info(
            "Proceso finalizado | Gestionados: %s | Errores: %s",
            enviados,
            errores
        )

    except Exception as error:

        logger.exception("Error general del programa")

        print(f"\nERROR GENERAL: {error}")


if __name__ == "__main__":
    main()

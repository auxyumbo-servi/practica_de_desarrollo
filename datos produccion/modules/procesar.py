
import pandas as pd


def convertir_numero(valor):

    if pd.isna(valor):
        return 0

    return float(valor)


def formatear_numero(valor):

    numero = convertir_numero(valor)

    return f"{numero:,.0f}".replace(",", ".")


def procesar_datos(df):

    registros = []

    for indice, fila in df.iterrows():

        try:

            # Verificar datos principales
            if pd.isna(fila["Nombre"]):
                raise ValueError("Nombre vacío")

            if pd.isna(fila["Fecha"]):
                raise ValueError("Fecha vacía")

            aforo = convertir_numero(
                fila["Aforo"]
            )

            datos = {
                "fila_excel": indice + 2,
                "contrato": fila["Contrato"],
                "nombre": str(fila["Nombre"]).strip(),
                "aforo": formatear_numero(aforo),
                "catidad": formatear_numero(fila["Cantidad"]),
                "valor_t": formatear_numero(fila["ValorT"]),
                "valor_m": formatear_numero(fila["ValorM"]),
                "unidad": str(fila["Unidad"]).strip(),
                "mini_activo": aforo > 0,
                "aforos": str(fila["Aforos"]).strip(),
                "asunto": str(fila["Asunto"]).strip(),
                "correo": str(fila["Correo"]).strip(),
                "copia": (
                    str(fila["Copia"]).strip()
                    if pd.notna(fila["Copia"])
                    else ""
                ),
                "archivo": (
                    str(fila["Archivo"]).strip()
                    if pd.notna(fila["Archivo"])
                    else ""
                )
            }

            registros.append(datos)

        except Exception as error:

            print(
                f"Error procesando fila {indice + 2}: {error}"
            )

    return registros

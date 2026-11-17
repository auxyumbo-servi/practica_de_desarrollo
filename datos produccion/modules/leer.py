import pandas as pd

from config import (
    ARCHIVO_EXCEL,
    HOJA_EXCEL,
    COLUMNAS_REQUERIDAS
)


def leer_excel():

    if not ARCHIVO_EXCEL.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ARCHIVO_EXCEL}"
        )

    df = pd.read_excel(
        ARCHIVO_EXCEL,
        sheet_name=HOJA_EXCEL
    )

    # Limpiar espacios de encabezados
    df.columns = df.columns.astype(str).str.strip()

    faltantes = [
        columna
        for columna in COLUMNAS_REQUERIDAS
        if columna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            f"Columnas faltantes: {faltantes}"
        )

    return df
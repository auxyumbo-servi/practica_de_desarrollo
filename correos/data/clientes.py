import pandas as pd

from config import ARCHIVO_EXCEL


def obtener_clientes():

    HOJA = "Produccion"

    df = pd.read_excel(
        ARCHIVO_EXCEL,
        sheet_name=HOJA
    )

    columnas = [
        "Nombre",
        "Contrato",
        "Subtotal",
        "Tipo_servicio",
        "Minicargador",
        "Recipiente"
    ]

    clientes = df[columnas].copy()

    # Siempre filtrar ESPECIAL
    clientes = clientes.loc[
        (clientes["Tipo_servicio"] == "ESPECIAL") &
        #(clientes["Nombre"] == user) &
        (clientes["Nombre"].notna())
    ]

    return clientes
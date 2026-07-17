import pandas as pd
from openpyxl import load_workbook


def exportar_meses_desde_columnas(
    df,
    archivo_plantilla="plantilla.xlsx",
    archivo_salida="reporte.xlsx",
    hoja="Reporte",
    fila_inicio=2,
    columna_cliente=1,
    columna_inicio=7,
    columnas_meses=("ABRIL", "MARZO", "FEBRERO", "ENERO")
):

    # ==========================
    # LIMPIEZA
    # ==========================
    df = df.copy()  
    df.columns = df.columns.astype(str).str.strip()

    if "CLIENTES" not in df.columns:
        raise ValueError(f"No existe columna CLIENTES. Columnas: {df.columns.tolist()}")

    # asegurar columnas de meses
    for c in columnas_meses:
        if c not in df.columns:
            df[c] = 0

    # limpiar clientes
    df["CLIENTES"] = df["CLIENTES"].astype(str).str.strip()

    # index para búsqueda rápida
    df = df.groupby("CLIENTES", as_index=False)[list(columnas_meses)].sum()
    df = df.set_index("CLIENTES")

    # ==========================
    # EXCEL
    # ==========================
    wb = load_workbook(archivo_plantilla)
    ws = wb[hoja]

    # encabezados
    for i, mes in enumerate(columnas_meses):
        ws.cell(
            row=fila_inicio - 1,
            column=columna_inicio + i,
            value=mes
        )

    # ==========================
    # ESCRIBIR DATOS
    # ==========================
    fila = fila_inicio

    while True:

        cliente = ws.cell(row=fila, column=columna_cliente).value

        if cliente is None:
            break

        cliente = str(cliente).strip()

        if cliente in df.index:

            for i, mes in enumerate(columnas_meses):

                valor = df.loc[cliente, mes]

                ws.cell(
                    row=fila,
                    column=columna_inicio + i,
                    value=float(valor)
                )

        fila += 1

    wb.save(archivo_salida)

    print("Excel generado correctamente")
import pandas as pd
from openpyxl import load_workbook


def exportar_por_meses(
    df,
    mes_inicio=1,
    cantidad_meses=4,
    archivo_plantilla="plantilla.xlsx",
    archivo_salida="reporte.xlsx",
    hoja="Reporte",
    fila_inicio=2,
    columna_valor=1,
    columna_inicio=7
):

    # ==========================
    # LIMPIEZA DE DATOS
    # ==========================
    df = df.copy()
    df.columns = df.columns.str.strip()

    if "fecha" not in df.columns:
        raise ValueError("No existe la columna 'fecha' en el DataFrame")

    if "Tarifa" not in df.columns:
        raise ValueError(f"No existe la columna 'Tarifa'. Columnas: {df.columns.tolist()}")

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["mes_numero"] = df["fecha"].dt.month

    df["Tarifa"] = pd.to_numeric(df["Tarifa"], errors="coerce").fillna(0)

    # ==========================
    # MESES
    # ==========================
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo",
        4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre",
        10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    # ==========================
    # MESES SELECCIONADOS (HACIA ATRÁS)
    # ==========================
    meses_seleccionados = [
        ((mes_inicio - i - 1) % 12) + 1
        for i in range(cantidad_meses)
    ]

    # ==========================
    # FILTRAR DATA
    # ==========================
    df = df[df["mes_numero"].isin(meses_seleccionados)]

    # ==========================
    # AGRUPAR POR CLIENTE Y MES
    # ==========================
    tabla = df.groupby(
    ["Nombre_final", "mes_numero"]
    )[columna_valor].sum().unstack(fill_value=0)

    # convertir meses a nombres
    tabla.columns = [meses[m] for m in tabla.columns]

    # respetar orden plantilla (mes_inicio → hacia atrás)
    columnas_meses = [meses[m] for m in meses_seleccionados]

    tabla = tabla.reindex(columns=columnas_meses, fill_value=0)

    # ==========================
    # CARGAR EXCEL
    # ==========================
    wb = load_workbook(archivo_plantilla)
    ws = wb[hoja]

    # ==========================
    # ESCRIBIR ENCABEZADOS
    # ==========================
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

        if cliente in tabla.index:

            for i, mes in enumerate(columnas_meses):

                valor = tabla.loc[cliente, mes] if mes in tabla.columns else 0

                ws.cell(
                    row=fila,
                    column=columna_inicio + i,
                    value=float(valor)
                )

        fila += 1

    wb.save(archivo_salida)

    print("Excel generado correctamente")
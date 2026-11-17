from __future__ import annotations

import re
import shutil
import unicodedata
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.worksheet import Worksheet

from config_reporte import (
    ARCHIVO_PLANTILLA,
    ARCHIVO_FUENTE,
    ARCHIVO_SALIDA,
    CANTIDAD_MESES_REPORTE,
    CLIENTES_INCLUIDOS,
    ETIQUETAS_COLUMNAS,
    HOJAS_REPORTE,
    HOJA_MES_ACTUAL,
    HOJA_MESES_ANTERIORES,
    PLACAS_VEHICULOS,
    PERIODO_REPORTE,
    TABLAS_EXCEL,
)
from generar_informe import CLIENT_RULES, normalize_columns, normalize_text, rule_rows


def _normalizar_etiqueta(valor: object) -> str:
    texto = unicodedata.normalize("NFKD", str(valor))
    texto = "".join(caracter for caracter in texto if not unicodedata.combining(caracter))
    return re.sub(r"[^a-z0-9]+", "_", texto.casefold()).strip("_")


def _normalizar_columnas(dataframe: pd.DataFrame) -> pd.DataFrame:
    resultado = dataframe.copy()
    resultado.columns = [_normalizar_etiqueta(columna) for columna in resultado.columns]
    return resultado


def obtener_dataframes_mensuales(
    archivo_fuente: Path = ARCHIVO_FUENTE,
    periodo_reporte: str = PERIODO_REPORTE,
) -> dict[pd.Period, pd.DataFrame]:
    periodo_actual = pd.Period(periodo_reporte, freq="M")
    produccion = _normalizar_columnas(
        pd.read_excel(
            archivo_fuente,
            sheet_name=HOJA_MES_ACTUAL,
            engine="openpyxl",
        )
    )
    historico = _normalizar_columnas(
        pd.read_excel(
            archivo_fuente,
            sheet_name=HOJA_MESES_ANTERIORES,
            engine="openpyxl",
        )
    )
    columna_fecha = _normalizar_etiqueta(ETIQUETAS_COLUMNAS["fecha"])

    frames_por_mes: dict[pd.Period, pd.DataFrame] = {}
    for desplazamiento in range(CANTIDAD_MESES_REPORTE):
        periodo = periodo_actual - desplazamiento
        nombre_hoja = HOJA_MES_ACTUAL if desplazamiento == 0 else HOJA_MESES_ANTERIORES
        datos = produccion if desplazamiento == 0 else historico
        if columna_fecha not in datos.columns:
            raise ValueError(
                f"No se encontró la columna '{ETIQUETAS_COLUMNAS['fecha']}' "
                f"en la hoja '{nombre_hoja}'."
            )

        fechas = pd.to_datetime(datos[columna_fecha], errors="coerce")
        dataframe_mes = datos.loc[fechas.dt.to_period("M").eq(periodo)].copy()
        if dataframe_mes.empty:
            raise ValueError(
                f"No hay registros para {periodo} en la hoja '{nombre_hoja}'."
            )
        frames_por_mes[periodo] = dataframe_mes

    return frames_por_mes


def obtener_dataframes_empresas(
    frames_por_mes: dict[pd.Period, pd.DataFrame],
) -> dict[pd.Period, pd.DataFrame]:
    reglas_por_cliente = {
        normalize_text(regla.label): regla
        for regla in CLIENT_RULES
    }
    etiquetas_cliente = [normalize_text(nombre) for nombre in CLIENTES_INCLUIDOS]
    etiquetas_sin_regla = sorted(set(etiquetas_cliente).difference(reglas_por_cliente))
    if etiquetas_sin_regla:
        raise ValueError(
            "Faltan reglas para excluir estos clientes del cuadro Empresas: "
            + ", ".join(etiquetas_sin_regla)
        )

    dataframes_empresas: dict[pd.Period, pd.DataFrame] = {}
    for periodo, dataframe_mes in frames_por_mes.items():
        datos = normalize_columns(dataframe_mes)
        mascara_clientes = pd.Series(False, index=datos.index)
        for etiqueta in etiquetas_cliente:
            filas_cliente = rule_rows(datos, reglas_por_cliente[etiqueta])
            mascara_clientes.loc[filas_cliente.index] = True

        filas_empresas = datos.loc[
            ~mascara_clientes & datos["empresa"].map(normalize_text).ne("")
        ]
        agrupado = (
            filas_empresas.groupby("empresa")
            .agg(
                TARIFA=("tarifa", "sum"),
                SUBTOTAL=("subtotal", "sum"),
            )
            .reset_index()
            .rename(columns={"empresa": "EMPRESA"})
        )
        agrupado = agrupado.sort_values("EMPRESA", key=lambda columna: columna.map(normalize_text))
        dataframes_empresas[periodo] = agrupado.reset_index(drop=True)

    return dataframes_empresas


def _sumar_columna(dataframe: pd.DataFrame, columna: str) -> float:
    valores = pd.to_numeric(dataframe[columna], errors="coerce")
    total = valores.sum(min_count=1)
    return 0.0 if pd.isna(total) else float(total)


def _construir_dataframe_clientes(
    frames_por_mes: dict[pd.Period, pd.DataFrame],
) -> pd.DataFrame:
    reglas = {normalize_text(regla.label): regla for regla in CLIENT_RULES}
    resultado: list[dict[str, object]] = []
    for periodo, dataframe_mes in frames_por_mes.items():
        datos = normalize_columns(dataframe_mes)
        for etiqueta in CLIENTES_INCLUIDOS:
            regla = reglas[normalize_text(etiqueta)]
            filas = rule_rows(datos, regla)
            resultado.append(
                {
                    "CLIENTE": etiqueta.strip(),
                    "PERIODO": str(periodo),
                    "VIAJES": int(filas["aforo"].nunique(dropna=True)),
                    "SUBTOTAL": _sumar_columna(filas, "subtotal"),
                    "TARIFA": _sumar_columna(filas, "tarifa"),
                }
            )
    return pd.DataFrame(
        resultado,
        columns=("CLIENTE", "PERIODO", "VIAJES", "SUBTOTAL", "TARIFA"),
    )


def _construir_dataframe_vehiculos(
    frames_por_mes: dict[pd.Period, pd.DataFrame],
) -> pd.DataFrame:
    resultado: list[dict[str, object]] = []
    for periodo, dataframe_mes in frames_por_mes.items():
        datos = normalize_columns(dataframe_mes)
        datos["placa_normalizada"] = datos["placa"].map(normalize_text)
        for placa in PLACAS_VEHICULOS:
            filas = datos.loc[datos["placa_normalizada"].eq(normalize_text(placa))]
            fechas = pd.to_datetime(filas["fecha"], errors="coerce").dropna()
            resultado.append(
                {
                    "VEHICULO": placa,
                    "PERIODO": str(periodo),
                    "DIAS_OPERACION": int(fechas.dt.normalize().nunique()),
                    "VIAJES": int(filas["aforo"].nunique(dropna=True)),
                    "FAVORES": int(
                        filas["nombre"].map(normalize_text).eq("FAVOR").sum()
                    ),
                    "TARIFA": _sumar_columna(filas, "tarifa"),
                }
            )
    return pd.DataFrame(
        resultado,
        columns=(
            "VEHICULO",
            "PERIODO",
            "DIAS_OPERACION",
            "VIAJES",
            "FAVORES",
            "TARIFA",
        ),
    )


def _construir_dataframe_alquileres(
    frames_por_mes: dict[pd.Period, pd.DataFrame],
) -> pd.DataFrame:
    filas_alquiler: list[pd.DataFrame] = []
    for periodo, dataframe_mes in frames_por_mes.items():
        datos = normalize_columns(dataframe_mes)
        horas = pd.to_numeric(datos["hh_alquiler"], errors="coerce")
        fecha = pd.to_datetime(datos["fecha"], errors="coerce")
        alquileres_mes = datos.loc[horas.notna() & fecha.notna()].copy()
        if alquileres_mes.empty:
            continue
        alquileres_mes["PERIODO"] = str(periodo)
        alquileres_mes["HH_ALQUILER"] = pd.to_numeric(
            alquileres_mes["hh_alquiler"], errors="coerce"
        )
        alquileres_mes["FECHA"] = fecha.loc[alquileres_mes.index]
        alquileres_mes["TARIFA"] = pd.to_numeric(
            alquileres_mes["tarifa"], errors="coerce"
        )
        alquileres_mes = alquileres_mes.rename(
            columns={
                "nombre": "CLIENTE",
                "placa": "VEHICULO",
                "empresa": "EMPRESA",
                "aforo": "AFORO",
            }
        )
        filas_alquiler.append(
            alquileres_mes[
                [
                    "PERIODO",
                    "FECHA",
                    "CLIENTE",
                    "EMPRESA",
                    "VEHICULO",
                    "AFORO",
                    "HH_ALQUILER",
                    "TARIFA",
                ]
            ]
        )

    columnas = (
        "PERIODO",
        "FECHA",
        "CLIENTE",
        "EMPRESA",
        "VEHICULO",
        "AFORO",
        "HH_ALQUILER",
        "TARIFA",
    )
    if not filas_alquiler:
        return pd.DataFrame(columns=columnas)
    return pd.concat(filas_alquiler, ignore_index=True).loc[:, columnas]


def construir_dataframes_reporte(
    frames_por_mes: dict[pd.Period, pd.DataFrame],
) -> dict[str, pd.DataFrame]:
    return {
        "clientes": _construir_dataframe_clientes(frames_por_mes),
        "empresas": pd.concat(
            [
                dataframe.assign(PERIODO=str(periodo))
                for periodo, dataframe in obtener_dataframes_empresas(
                    frames_por_mes
                ).items()
            ],
            ignore_index=True,
        ).loc[:, ["PERIODO", "EMPRESA", "TARIFA", "SUBTOTAL"]],
        "vehiculos": _construir_dataframe_vehiculos(frames_por_mes),
        "alquileres": _construir_dataframe_alquileres(frames_por_mes),
    }


def _valor_excel(valor: object) -> object:
    if pd.isna(valor):
        return None
    if isinstance(valor, pd.Timestamp):
        return valor.to_pydatetime()
    if hasattr(valor, "item"):
        return valor.item()
    return valor


def _escribir_tabla(
    hoja: Worksheet,
    dataframe: pd.DataFrame,
    nombre_tabla: str,
) -> None:
    hoja.append(list(dataframe.columns))
    for fila in dataframe.itertuples(index=False, name=None):
        hoja.append([_valor_excel(valor) for valor in fila])

    if dataframe.columns.empty:
        raise ValueError(f"No hay encabezados para la tabla {nombre_tabla}.")
    ultima_columna = hoja.max_column
    ultima_fila = max(hoja.max_row, 2)
    referencia = f"A1:{hoja.cell(row=1, column=ultima_columna).column_letter}{ultima_fila}"
    tabla = Table(displayName=nombre_tabla, ref=referencia)
    tabla.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    hoja.add_table(tabla)
    hoja.freeze_panes = "A2"

    for celda in hoja[1]:
        celda.font = Font(bold=True, color="FFFFFF")
        celda.fill = PatternFill("solid", fgColor="4472C4")
    for columna in hoja.columns:
        letra = columna[0].column_letter
        ancho = max(
            (len(str(celda.value)) for celda in columna if celda.value is not None),
            default=10,
        )
        hoja.column_dimensions[letra].width = min(max(ancho + 2, 12), 32)
    for fila in hoja.iter_rows(min_row=2):
        for celda in fila:
            encabezado = str(hoja.cell(row=1, column=celda.column).value)
            if encabezado in {"TARIFA"}:
                celda.number_format = '#,##0.00;[Red]-#,##0.00'
            elif encabezado in {"SUBTOTAL"}:
                celda.number_format = '#,##0.000;[Red]-#,##0.000'
            elif encabezado == "FECHA":
                celda.number_format = "dd/mm/yyyy"


def exportar_copia_plantilla(
    dataframes: dict[str, pd.DataFrame],
    archivo_salida: Path = ARCHIVO_SALIDA,
    archivo_plantilla: Path = ARCHIVO_PLANTILLA,
    archivo_fuente: Path = ARCHIVO_FUENTE,
) -> Path:
    salida = archivo_salida.resolve()
    if salida in {archivo_plantilla.resolve(), archivo_fuente.resolve()}:
        raise ValueError("La salida debe ser distinta a la plantilla y al archivo fuente.")
    if set(dataframes) != set(HOJAS_REPORTE):
        raise ValueError(
            "Se requieren los cuatro DataFrames configurados: "
            + ", ".join(HOJAS_REPORTE)
        )

    salida.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(archivo_plantilla, salida)
    libro = load_workbook(salida)
    for clave, nombre_hoja in HOJAS_REPORTE.items():
        if nombre_hoja in libro.sheetnames:
            del libro[nombre_hoja]
        hoja = libro.create_sheet(nombre_hoja)
        _escribir_tabla(hoja, dataframes[clave], TABLAS_EXCEL[clave])
    libro.properties.subject = (
        f"Informe estructurado de {PERIODO_REPORTE}, "
        "datos mensuales en orden reciente a antiguo"
    )
    libro.save(salida)
    return salida


def mostrar_resumen(frames_por_mes: dict[pd.Period, pd.DataFrame]) -> None:
    for periodo, dataframe in frames_por_mes.items():
        fechas = pd.to_datetime(dataframe["fecha"], errors="coerce").dropna()
        fecha_final = fechas.max().date() if not fechas.empty else "sin fecha"
        print(f"{periodo}: {len(dataframe)} registros; último registro: {fecha_final}")


def main() -> None:
    frames_por_mes = obtener_dataframes_mensuales()
    mostrar_resumen(frames_por_mes)
    dataframes = construir_dataframes_reporte(frames_por_mes)
    archivo_generado = exportar_copia_plantilla(dataframes)
    print(f"\nCopia de la plantilla creada: {archivo_generado}")
    for clave, dataframe in dataframes.items():
        print(f"{HOJAS_REPORTE[clave]}: {len(dataframe)} filas")


if __name__ == "__main__":
    main()

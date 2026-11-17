from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE = BASE_DIR.parent / "historico.db"
DEFAULT_OUTPUT = BASE_DIR.parent / "Exportacion_tablas.xlsx"


@dataclass(frozen=True)
class ExportSheet:
    name: str
    query: str


EXPORT_SHEETS = (
    ExportSheet(
        "Usuarios",
        """
        SELECT
            u.nombre AS "Usuario",
            u.activo AS "Activo",
            (
                SELECT group_concat(et.nombre, ', ')
                FROM usuario_etiquetas ue
                JOIN etiquetas et ON et.id_etiqueta = ue.id_etiqueta
                WHERE ue.id_usuario = u.id_usuario
            ) AS "Etiquetas",
            (
                SELECT group_concat(e.nombre, ', ')
                FROM usuario_empresas ue
                JOIN empresas e ON e.id_empresa = ue.id_empresa
                WHERE ue.id_usuario = u.id_usuario
            ) AS "Empresas"
        FROM usuarios u
        ORDER BY u.nombre COLLATE NOCASE
        """,
    ),
    ExportSheet(
        "Empresas",
        """
        SELECT
            e.nombre AS "Empresa",
            e.activo AS "Activo",
            (
                SELECT group_concat(et.nombre, ', ')
                FROM empresa_etiquetas ee
                JOIN etiquetas et ON et.id_etiqueta = ee.id_etiqueta
                WHERE ee.id_empresa = e.id_empresa
            ) AS "Etiquetas"
        FROM empresas e
        ORDER BY e.nombre COLLATE NOCASE
        """,
    ),
    ExportSheet(
        "Placas",
        """
        SELECT
            p.placa AS "Placa",
            p.tipo AS "Tipo",
            p.alquiler AS "Alquiler",
            p.activo AS "Activo",
            (
                SELECT group_concat(et.nombre, ', ')
                FROM placa_etiquetas pe
                JOIN etiquetas et ON et.id_etiqueta = pe.id_etiqueta
                WHERE pe.id_placa = p.id_placa
            ) AS "Etiquetas"
        FROM placas p
        ORDER BY p.placa COLLATE NOCASE
        """,
    ),
    ExportSheet(
        "Etiquetas",
        """
        SELECT
            tipo_entidad AS "Tipo de entidad",
            nombre AS "Etiqueta",
            activo AS "Activo"
        FROM etiquetas
        ORDER BY tipo_entidad, nombre COLLATE NOCASE
        """,
    ),
    ExportSheet(
        "Usuario etiquetas",
        """
        SELECT u.nombre AS "Usuario", et.nombre AS "Etiqueta", et.activo AS "Etiqueta activa"
        FROM usuario_etiquetas ue
        JOIN usuarios u ON u.id_usuario = ue.id_usuario
        JOIN etiquetas et ON et.id_etiqueta = ue.id_etiqueta
        ORDER BY u.nombre COLLATE NOCASE, et.nombre COLLATE NOCASE
        """,
    ),
    ExportSheet(
        "Placa etiquetas",
        """
        SELECT p.placa AS "Placa", et.nombre AS "Etiqueta", et.activo AS "Etiqueta activa"
        FROM placa_etiquetas pe
        JOIN placas p ON p.id_placa = pe.id_placa
        JOIN etiquetas et ON et.id_etiqueta = pe.id_etiqueta
        ORDER BY p.placa COLLATE NOCASE, et.nombre COLLATE NOCASE
        """,
    ),
    ExportSheet(
        "Empresa etiquetas",
        """
        SELECT e.nombre AS "Empresa", et.nombre AS "Etiqueta", et.activo AS "Etiqueta activa"
        FROM empresa_etiquetas ee
        JOIN empresas e ON e.id_empresa = ee.id_empresa
        JOIN etiquetas et ON et.id_etiqueta = ee.id_etiqueta
        ORDER BY e.nombre COLLATE NOCASE, et.nombre COLLATE NOCASE
        """,
    ),
    ExportSheet(
        "Usuario empresas",
        """
        SELECT u.nombre AS "Usuario", e.nombre AS "Empresa"
        FROM usuario_empresas ue
        JOIN usuarios u ON u.id_usuario = ue.id_usuario
        JOIN empresas e ON e.id_empresa = ue.id_empresa
        ORDER BY u.nombre COLLATE NOCASE, e.nombre COLLATE NOCASE
        """,
    ),
    ExportSheet(
        "Historico",
        """
        SELECT
            h.fecha AS "Fecha",
            u.nombre AS "Usuario",
            p.placa AS "Placa",
            h.aforo AS "Aforo",
            h.recipiente AS "Recipiente",
            h.cantidad AS "Cantidad",
            h.subtotal AS "Subtotal",
            e.nombre AS "Empresa",
            h.tipo_servicio AS "Tipo servicio",
            h.valor AS "Valor",
            h.facturable AS "Facturable",
            h.minicargador AS "Minicargador",
            h.observacion AS "Observacion",
            h.mes AS "Mes",
            h.anio AS "Año",
            h.estado AS "Estado",
            h.tarifa AS "Tarifa",
            h.horas_alquiler AS "Horas alquiler"
        FROM historico h
        LEFT JOIN usuarios u ON u.id_usuario = h.id_usuario
        LEFT JOIN placas p ON p.id_placa = h.id_placa
        LEFT JOIN empresas e ON e.id_empresa = h.id_empresa
        ORDER BY h.fila_origen
        """,
    ),
    ExportSheet(
        "Historico tipo servicio",
        """
        SELECT
            h.fecha AS "Fecha",
            u.nombre AS "Usuario",
            p.placa AS "Placa",
            h.aforo AS "Aforo",
            h.recipiente AS "Recipiente",
            h.cantidad AS "Cantidad",
            h.subtotal AS "Subtotal",
            e.nombre AS "Empresa",
            h.tipo_servicio AS "Tipo servicio",
            h.valor AS "Valor",
            h.facturable AS "Facturable",
            h.minicargador AS "Minicargador",
            h.observacion AS "Observacion",
            h.mes AS "Mes",
            h.anio AS "Año",
            h.estado AS "Estado",
            h.tarifa AS "Tarifa",
            h.horas_alquiler AS "Horas alquiler"
        FROM historico_tipo_servicio h
        LEFT JOIN usuarios u ON u.id_usuario = h.id_usuario
        LEFT JOIN placas p ON p.id_placa = h.id_placa
        LEFT JOIN empresas e ON e.id_empresa = h.id_empresa
        ORDER BY h.fila_origen
        """,
    ),
)


def _validate_database(connection: sqlite3.Connection) -> None:
    existing_tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    required_tables = {
        "usuarios",
        "empresas",
        "placas",
        "etiquetas",
        "usuario_etiquetas",
        "placa_etiquetas",
        "empresa_etiquetas",
        "usuario_empresas",
        "historico",
        "historico_tipo_servicio",
    }
    missing = sorted(required_tables - existing_tables)
    if missing:
        raise ValueError(
            "La base no contiene las tablas requeridas: " + ", ".join(missing)
        )


def _write_sheet(
    connection: sqlite3.Connection,
    workbook: Workbook,
    sheet_spec: ExportSheet,
) -> None:
    cursor = connection.execute(sheet_spec.query)
    worksheet = workbook.create_sheet(sheet_spec.name)
    headers = [description[0] for description in cursor.description]
    worksheet.append(headers)

    for row in cursor:
        worksheet.append(
            [
                _excel_text(value) if isinstance(value, str) else value
                for value in row
            ]
        )

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    worksheet.row_dimensions[1].height = 24
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="1F4E78")

    for column_index, header in enumerate(headers, start=1):
        sample_values = (
            worksheet.cell(row=row_index, column=column_index).value
            for row_index in range(2, min(worksheet.max_row, 101) + 1)
        )
        max_length = max(
            [len(str(header))]
            + [len(str(value)) for value in sample_values if value is not None]
        )
        worksheet.column_dimensions[get_column_letter(column_index)].width = min(
            max(max_length + 2, 12),
            50,
        )


def _excel_text(value: str) -> str:
    if value.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def exportar_tablas(
    database_path: Path = DEFAULT_DATABASE,
    output_path: Path = DEFAULT_OUTPUT,
) -> Path:
    database_path = Path(database_path).resolve(strict=True)
    output_path = Path(output_path).resolve()
    if database_path == output_path:
        raise ValueError("El archivo de exportación no puede sobrescribir la base SQLite.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    try:
        _validate_database(connection)
        workbook = Workbook()
        workbook.remove(workbook.active)
        try:
            for sheet_spec in EXPORT_SHEETS:
                _write_sheet(connection, workbook, sheet_spec)
            workbook.save(output_path)
        finally:
            workbook.close()
    finally:
        connection.close()

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta las tablas SQLite a Excel usando nombres en vez de IDs."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help="Archivo SQLite de origen.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Archivo XLSX de destino.",
    )
    arguments = parser.parse_args()
    output = exportar_tablas(arguments.database, arguments.output)
    print(f"Exportación completada: {output}")


if __name__ == "__main__":
    main()

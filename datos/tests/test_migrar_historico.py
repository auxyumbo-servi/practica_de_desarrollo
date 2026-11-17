from __future__ import annotations

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

import sys

from openpyxl import Workbook, load_workbook

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bk.exportar_tablas import EXPORT_SHEETS, exportar_tablas
from bk.migrar_historico import migrar_historico


HISTORY_HEADERS = (
    "Fecha",
    "Nombre",
    "Placa",
    "Aforo",
    "Recipiente",
    "Cantidad",
    "Subtotal",
    "Empresa",
    "Tipo_Servicio",
    "Valor",
    "Facturable",
    "Minicargador",
    "Observacion",
    "Mes",
    "A�o",
    "Estado",
    "Tarifa",
    "hh-alquiler",
)


class MigrarHistoricoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary_directory.name)
        self.source = self.directory / "fuente.xlsx"
        self.database = self.directory / "historico.db"
        self._create_workbook()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _create_workbook(self) -> None:
        workbook = Workbook()
        history = workbook.active
        history.title = "Historico"
        history.append(HISTORY_HEADERS)
        history.append(
            (
                "2026-01-03",
                "Usuario A",
                "AAA123",
                1,
                "Caneca",
                2,
                40,
                "Empresa A",
                "Ordinario",
                40,
                "SI",
                None,
                "Nota",
                "ENERO",
                2026,
                "PENDIENTE",
                20,
                None,
            )
        )
        history.append(
            (
                "2026-01-04",
                "Usuario B",
                None,
                2,
                "Caneca",
                1,
                30,
                "Empresa A",
                "Especial",
                30,
                "NO",
                None,
                None,
                "ENERO",
                2026,
                "PENDIENTE",
                30,
                None,
            )
        )
        history.append(
            (
                "2026-01-05",
                "Usuario B",
                None,
                2,
                "Caneca",
                1,
                30,
                "Empresa A",
                None,
                30,
                "NO",
                None,
                None,
                "ENERO",
                2026,
                "PENDIENTE",
                30,
                None,
            )
        )
        history.append((None,) * len(HISTORY_HEADERS))

        clients = workbook.create_sheet("clientes")
        clients.append(("Nombre_ID", "Nombre", "Contrato", "Empresa", "Clasificacion"))
        clients.append(("U-01", "Usuario A", None, "Empresa A", "user"))

        vehicles = workbook.create_sheet("vehiculos")
        vehicles.append(("placa", "tipo", "alquiler", "activo"))
        vehicles.append(("AAA123", "Compactador", None, "X"))
        workbook.save(self.source)
        workbook.close()

    def test_imports_related_entities_labels_and_all_history_rows(self) -> None:
        summary = migrar_historico(self.source, self.database)

        self.assertEqual(summary.filas_historico, 3)
        self.assertEqual(summary.filas_con_tipo_servicio_y_placa, 1)
        self.assertEqual(summary.usuarios, 2)
        self.assertEqual(summary.empresas, 1)
        self.assertEqual(summary.placas, 1)
        self.assertEqual(summary.etiquetas, 2)

        with closing(sqlite3.connect(self.database)) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            history = connection.execute(
                """
                SELECT COUNT(*), COUNT(id_usuario), COUNT(id_empresa), COUNT(id_placa)
                FROM historico
                """
            ).fetchone()
            self.assertEqual(history, (3, 3, 3, 1))
            service_history = connection.execute(
                """
                SELECT COUNT(*), COUNT(tipo_servicio), MIN(tipo_servicio), MAX(tipo_servicio)
                FROM historico_tipo_servicio
                """
            ).fetchone()
            self.assertEqual(service_history, (1, 1, "Ordinario", "Ordinario"))
            self.assertEqual(
                connection.execute(
                    """
                    SELECT COUNT(*)
                    FROM historico_tipo_servicio
                    WHERE tipo_servicio IS NULL
                    """
                ).fetchone()[0],
                0,
            )
            self.assertEqual(
                connection.execute(
                    """
                    SELECT COUNT(*)
                    FROM historico_tipo_servicio
                    WHERE id_placa IS NULL
                    """
                ).fetchone()[0],
                0,
            )
            self.assertEqual(
                connection.execute(
                    """
                    SELECT COUNT(*)
                    FROM historico h
                    LEFT JOIN historico_tipo_servicio hs USING (id_registro)
                    WHERE h.tipo_servicio IS NOT NULL
                      AND h.id_placa IS NOT NULL
                      AND hs.id_registro IS NULL
                    """
                ).fetchone()[0],
                0,
            )

            user = connection.execute(
                "SELECT id_usuario, codigo_origen, activo FROM usuarios WHERE nombre = ?",
                ("Usuario A",),
            ).fetchone()
            self.assertEqual(user[1:], ("U-01", 1))
            user_label = connection.execute(
                """
                SELECT e.nombre, e.tipo_entidad
                FROM usuario_etiquetas ue
                JOIN etiquetas e USING (id_etiqueta)
                WHERE ue.id_usuario = ?
                """,
                (user[0],),
            ).fetchone()
            self.assertEqual(user_label, ("user", "usuario"))

            plate = connection.execute(
                "SELECT activo FROM placas WHERE placa = ?", ("AAA123",)
            ).fetchone()
            self.assertEqual(plate, (1,))
            plate_label = connection.execute(
                """
                SELECT e.nombre, e.tipo_entidad
                FROM placa_etiquetas pe
                JOIN etiquetas e USING (id_etiqueta)
                """
            ).fetchone()
            self.assertEqual(plate_label, ("Compactador", "placa"))
            self.assertEqual(
                connection.execute("PRAGMA foreign_key_check").fetchall(),
                [],
            )

    def test_migration_is_idempotent(self) -> None:
        migrar_historico(self.source, self.database)
        migrar_historico(self.source, self.database)

        with closing(sqlite3.connect(self.database)) as connection:
            self.assertEqual(
                connection.execute("SELECT COUNT(*) FROM historico").fetchone()[0],
                3,
            )
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM historico_tipo_servicio"
                ).fetchone()[0],
                1,
            )
            self.assertEqual(
                connection.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0],
                2,
            )

    def test_dry_run_does_not_create_database(self) -> None:
        summary = migrar_historico(self.source, self.database, dry_run=True)

        self.assertEqual(summary.filas_historico, 3)
        self.assertEqual(summary.filas_con_tipo_servicio_y_placa, 1)
        self.assertFalse(self.database.exists())

    def test_export_uses_names_instead_of_internal_ids(self) -> None:
        migrar_historico(self.source, self.database)
        output = self.directory / "exportacion.xlsx"

        self.assertEqual(exportar_tablas(self.database, output), output.resolve())

        workbook = load_workbook(output, read_only=True, data_only=True)
        try:
            self.assertEqual(
                workbook.sheetnames,
                [sheet.name for sheet in EXPORT_SHEETS],
            )
            for sheet in workbook.worksheets:
                headers = next(sheet.iter_rows(min_row=1, max_row=1, values_only=True))
                self.assertFalse(
                    any(
                        str(header).casefold().startswith(("id_", "fila_origen"))
                        for header in headers
                        if header is not None
                    ),
                    msg=f"La hoja {sheet.title} exportó IDs internos.",
                )

            history = workbook["Historico"]
            rows = list(history.iter_rows(min_row=2, values_only=True))
            headers = next(history.iter_rows(min_row=1, max_row=1, values_only=True))
            user_column = headers.index("Usuario")
            company_column = headers.index("Empresa")
            plate_column = headers.index("Placa")
            self.assertEqual(rows[0][user_column], "Usuario A")
            self.assertEqual(rows[0][company_column], "Empresa A")
            self.assertEqual(rows[0][plate_column], "AAA123")

            filtered_history = workbook["Historico tipo servicio"]
            filtered_rows = list(
                filtered_history.iter_rows(min_row=2, values_only=True)
            )
            self.assertEqual(len(filtered_rows), 1)
            self.assertTrue(all(row[8] is not None for row in filtered_rows))
            self.assertTrue(all(row[2] is not None for row in filtered_rows))
        finally:
            workbook.close()


if __name__ == "__main__":
    unittest.main()

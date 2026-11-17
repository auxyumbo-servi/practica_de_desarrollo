from __future__ import annotations

import argparse
import json
import re
import sqlite3
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date, datetime, time
from pathlib import Path
from typing import Any

from openpyxl import load_workbook


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = BASE_DIR.parent / "AFOROS DEL 2026.xlsm"
DEFAULT_DATABASE = BASE_DIR.parent / "historico.db"
SCHEMA_FILE = BASE_DIR / "schema.sql"

HISTORICO_COLUMNS = (
    "fecha",
    "nombre",
    "placa",
    "aforo",
    "recipiente",
    "cantidad",
    "subtotal",
    "empresa",
    "tipo_servicio",
    "valor",
    "facturable",
    "minicargador",
    "observacion",
    "mes",
    "anio",
    "estado",
    "tarifa",
    "horas_alquiler",
)

HISTORICO_ALIASES = {
    "ano": "anio",
    "anio": "anio",
    "hh_alquiler": "horas_alquiler",
}


@dataclass(frozen=True)
class MigrationSummary:
    filas_historico: int
    filas_con_tipo_servicio_y_placa: int
    usuarios: int
    empresas: int
    placas: int
    etiquetas: int


def _header_key(value: Any) -> str:
    text = str(value).strip().replace("\ufffd", "n").replace("�", "n")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "_", text.casefold()).strip("_")


def _text(value: Any) -> str | None:
    if value is None:
        return None
    result = " ".join(str(value).split())
    return result or None


def _key(value: str) -> str:
    return unicodedata.normalize("NFKC", " ".join(value.split())).casefold()


def _db_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, (str, int, float, bytes)):
        return value
    return str(value)


def _status(value: Any, default: int = 1) -> int:
    text = _text(value)
    if text is None:
        return default
    normalized = _header_key(text)
    if normalized in {"x", "1", "si", "s", "true", "activo", "activa"}:
        return 1
    if normalized in {"0", "no", "n", "false", "inactivo", "inactiva"}:
        return 0
    raise ValueError(f"Valor de estado no reconocido en el catálogo vehicular: {text!r}")


def _column_indexes(
    worksheet: Any,
    required: tuple[str, ...],
    aliases: dict[str, str] | None = None,
) -> dict[str, int]:
    aliases = aliases or {}
    indexes: dict[str, int] = {}
    for index, value in enumerate(next(worksheet.iter_rows(min_row=1, max_row=1, values_only=True))):
        if value is None:
            continue
        name = _header_key(value)
        name = aliases.get(name, name)
        indexes.setdefault(name, index)
    missing = [column for column in required if column not in indexes]
    if missing:
        raise ValueError(
            f"La hoja {worksheet.title!r} no contiene las columnas requeridas: "
            + ", ".join(missing)
        )
    return indexes


def _cell(row: tuple[Any, ...], indexes: dict[str, int], column: str) -> Any:
    index = indexes[column]
    return row[index] if index < len(row) else None


def _ensure_usuario(
    connection: sqlite3.Connection,
    name: str | None,
    codigo_origen: Any = None,
) -> int | None:
    nombre = _text(name)
    if nombre is None:
        return None
    key = _key(nombre)
    connection.execute(
        """
        INSERT INTO usuarios (nombre, clave, codigo_origen)
        VALUES (?, ?, ?)
        ON CONFLICT (clave) DO UPDATE SET
            nombre = excluded.nombre,
            codigo_origen = COALESCE(excluded.codigo_origen, usuarios.codigo_origen)
        """,
        (nombre, key, _text(codigo_origen)),
    )
    row = connection.execute(
        "SELECT id_usuario FROM usuarios WHERE clave = ?", (key,)
    ).fetchone()
    return int(row[0])


def _ensure_empresa(
    connection: sqlite3.Connection,
    name: str | None,
) -> int | None:
    nombre = _text(name)
    if nombre is None:
        return None
    key = _key(nombre)
    connection.execute(
        """
        INSERT INTO empresas (nombre, clave)
        VALUES (?, ?)
        ON CONFLICT (clave) DO UPDATE SET nombre = excluded.nombre
        """,
        (nombre, key),
    )
    row = connection.execute(
        "SELECT id_empresa FROM empresas WHERE clave = ?", (key,)
    ).fetchone()
    return int(row[0])


def _ensure_placa(
    connection: sqlite3.Connection,
    plate: str | None,
    tipo: Any = None,
    alquiler: Any = None,
    activo: int = 1,
) -> int | None:
    placa = _text(plate)
    if placa is None:
        return None
    key = _key(placa)
    connection.execute(
        """
        INSERT INTO placas (placa, clave, tipo, alquiler, activo)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT (clave) DO UPDATE SET
            placa = excluded.placa,
            tipo = COALESCE(excluded.tipo, placas.tipo),
            alquiler = COALESCE(excluded.alquiler, placas.alquiler)
        """,
        (placa, key, _db_value(tipo), _db_value(alquiler), activo),
    )
    row = connection.execute(
        "SELECT id_placa FROM placas WHERE clave = ?", (key,)
    ).fetchone()
    return int(row[0])


def _ensure_etiqueta(
    connection: sqlite3.Connection,
    tipo_entidad: str,
    label: Any,
) -> int | None:
    nombre = _text(label)
    if nombre is None:
        return None
    key = _key(nombre)
    connection.execute(
        """
        INSERT INTO etiquetas (tipo_entidad, nombre, clave)
        VALUES (?, ?, ?)
        ON CONFLICT (tipo_entidad, clave) DO UPDATE SET nombre = excluded.nombre
        """,
        (tipo_entidad, nombre, key),
    )
    row = connection.execute(
        """
        SELECT id_etiqueta FROM etiquetas
        WHERE tipo_entidad = ? AND clave = ?
        """,
        (tipo_entidad, key),
    ).fetchone()
    return int(row[0])


def _asociar_etiqueta(
    connection: sqlite3.Connection,
    tipo_entidad: str,
    entity_id: int | None,
    label: Any,
) -> None:
    if entity_id is None:
        return
    label_id = _ensure_etiqueta(connection, tipo_entidad, label)
    if label_id is None:
        return
    table, id_column = {
        "usuario": ("usuario_etiquetas", "id_usuario"),
        "placa": ("placa_etiquetas", "id_placa"),
        "empresa": ("empresa_etiquetas", "id_empresa"),
    }[tipo_entidad]
    connection.execute(
        f"INSERT OR IGNORE INTO {table} ({id_column}, id_etiqueta) VALUES (?, ?)",
        (entity_id, label_id),
    )


def _upsert_historico(
    connection: sqlite3.Connection,
    source_row: int,
    values: dict[str, Any],
    user_id: int | None,
    plate_id: int | None,
    company_id: int | None,
) -> None:
    connection.execute(
        """
        INSERT INTO historico (
            fila_origen, id_usuario, id_placa, id_empresa, fecha, aforo,
            recipiente, cantidad, subtotal, tipo_servicio, valor, facturable,
            minicargador, observacion, mes, anio, estado, tarifa, horas_alquiler
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (fila_origen) DO UPDATE SET
            id_usuario = excluded.id_usuario,
            id_placa = excluded.id_placa,
            id_empresa = excluded.id_empresa,
            fecha = excluded.fecha,
            aforo = excluded.aforo,
            recipiente = excluded.recipiente,
            cantidad = excluded.cantidad,
            subtotal = excluded.subtotal,
            tipo_servicio = excluded.tipo_servicio,
            valor = excluded.valor,
            facturable = excluded.facturable,
            minicargador = excluded.minicargador,
            observacion = excluded.observacion,
            mes = excluded.mes,
            anio = excluded.anio,
            estado = excluded.estado,
            tarifa = excluded.tarifa,
            horas_alquiler = excluded.horas_alquiler
        """,
        (
            source_row,
            user_id,
            plate_id,
            company_id,
            _db_value(values["fecha"]),
            _db_value(values["aforo"]),
            _db_value(values["recipiente"]),
            _db_value(values["cantidad"]),
            _db_value(values["subtotal"]),
            _db_value(values["tipo_servicio"]),
            _db_value(values["valor"]),
            _db_value(values["facturable"]),
            _db_value(values["minicargador"]),
            _db_value(values["observacion"]),
            _db_value(values["mes"]),
            _db_value(values["anio"]),
            _db_value(values["estado"]),
            _db_value(values["tarifa"]),
            _db_value(values["horas_alquiler"]),
        ),
    )


def _actualizar_historico_tipo_servicio(connection: sqlite3.Connection) -> None:
    connection.execute("DELETE FROM historico_tipo_servicio")
    connection.execute(
        """
        INSERT INTO historico_tipo_servicio (
            id_registro, fila_origen, id_usuario, id_placa, id_empresa, fecha,
            aforo, recipiente, cantidad, subtotal, tipo_servicio, valor,
            facturable, minicargador, observacion, mes, anio, estado, tarifa,
            horas_alquiler
        )
        SELECT
            id_registro, fila_origen, id_usuario, id_placa, id_empresa, fecha,
            aforo, recipiente, cantidad, subtotal, tipo_servicio, valor,
            facturable, minicargador, observacion, mes, anio, estado, tarifa,
            horas_alquiler
        FROM historico
        WHERE tipo_servicio IS NOT NULL
          AND id_placa IS NOT NULL
        """
    )


def migrar_historico(
    source_path: Path = DEFAULT_SOURCE,
    database_path: Path = DEFAULT_DATABASE,
    dry_run: bool = False,
) -> MigrationSummary:
    source_path = Path(source_path).resolve(strict=True)
    database_path = Path(database_path).resolve()
    if source_path == database_path:
        raise ValueError("El archivo de base de datos no puede sobrescribir el Excel de origen.")
    if not SCHEMA_FILE.is_file():
        raise FileNotFoundError(f"No se encontró el esquema SQL: {SCHEMA_FILE}")

    workbook = load_workbook(source_path, read_only=True, data_only=True)
    required_sheets = {"Historico", "clientes", "vehiculos"}
    missing_sheets = required_sheets.difference(workbook.sheetnames)
    if missing_sheets:
        workbook.close()
        raise ValueError(
            "Faltan hojas requeridas en el Excel: " + ", ".join(sorted(missing_sheets))
        )

    database: str | Path = ":memory:" if dry_run else database_path
    if not dry_run:
        database_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        connection = sqlite3.connect(database)
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            schema = SCHEMA_FILE.read_text(encoding="utf-8")
            connection.executescript("BEGIN IMMEDIATE;\n" + schema)

            clients = workbook["clientes"]
            client_columns = _column_indexes(
                clients,
                ("nombre", "nombre_id", "empresa", "clasificacion"),
            )
            for row in clients.iter_rows(min_row=2, values_only=True):
                name = _text(_cell(row, client_columns, "nombre"))
                if name is None:
                    continue
                user_id = _ensure_usuario(
                    connection,
                    name,
                    _cell(row, client_columns, "nombre_id"),
                )
                company_id = _ensure_empresa(
                    connection,
                    _cell(row, client_columns, "empresa"),
                )
                if company_id is not None and user_id is not None:
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO usuario_empresas (id_usuario, id_empresa)
                        VALUES (?, ?)
                        """,
                        (user_id, company_id),
                    )
                _asociar_etiqueta(
                    connection,
                    "usuario",
                    user_id,
                    _cell(row, client_columns, "clasificacion"),
                )

            vehicles = workbook["vehiculos"]
            vehicle_columns = _column_indexes(
                vehicles,
                ("placa", "tipo", "alquiler", "activo"),
            )
            for row in vehicles.iter_rows(min_row=2, values_only=True):
                plate = _text(_cell(row, vehicle_columns, "placa"))
                if plate is None:
                    continue
                plate_id = _ensure_placa(
                    connection,
                    plate,
                    _cell(row, vehicle_columns, "tipo"),
                    _cell(row, vehicle_columns, "alquiler"),
                    _status(_cell(row, vehicle_columns, "activo")),
                )
                _asociar_etiqueta(
                    connection,
                    "placa",
                    plate_id,
                    _cell(row, vehicle_columns, "tipo"),
                )

            history = workbook["Historico"]
            history_columns = _column_indexes(
                history,
                HISTORICO_COLUMNS,
                HISTORICO_ALIASES,
            )
            history_rows = 0
            for source_row, row in enumerate(
                history.iter_rows(min_row=2, values_only=True),
                start=2,
            ):
                values = {
                    column: _cell(row, history_columns, column)
                    for column in HISTORICO_COLUMNS
                }
                if all(value is None or value == "" for value in values.values()):
                    continue
                history_rows += 1
                user_id = _ensure_usuario(connection, values["nombre"])
                plate_id = _ensure_placa(connection, _text(values["placa"]))
                company_id = _ensure_empresa(connection, _text(values["empresa"]))
                if user_id is not None and company_id is not None:
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO usuario_empresas (id_usuario, id_empresa)
                        VALUES (?, ?)
                        """,
                        (user_id, company_id),
                    )
                _upsert_historico(
                    connection,
                    source_row,
                    values,
                    user_id,
                    plate_id,
                    company_id,
                )

            _actualizar_historico_tipo_servicio(connection)

            violations = connection.execute("PRAGMA foreign_key_check").fetchall()
            if violations:
                raise sqlite3.IntegrityError(
                    f"La migración produjo {len(violations)} relaciones inválidas."
                )

            summary = MigrationSummary(
                filas_historico=history_rows,
                filas_con_tipo_servicio_y_placa=connection.execute(
                    "SELECT COUNT(*) FROM historico_tipo_servicio"
                ).fetchone()[0],
                usuarios=connection.execute(
                    "SELECT COUNT(*) FROM usuarios"
                ).fetchone()[0],
                empresas=connection.execute(
                    "SELECT COUNT(*) FROM empresas"
                ).fetchone()[0],
                placas=connection.execute("SELECT COUNT(*) FROM placas").fetchone()[0],
                etiquetas=connection.execute(
                    "SELECT COUNT(*) FROM etiquetas"
                ).fetchone()[0],
            )
            if dry_run:
                connection.rollback()
            else:
                connection.commit()
            return summary
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
    finally:
        workbook.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migra la hoja Historico del Excel a una base SQLite relacionada."
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Archivo XLSM.")
    parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help="Archivo SQLite de destino (por defecto, datos/historico.db).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida y cuenta los registros sin escribir la base de datos.",
    )
    args = parser.parse_args()

    summary = migrar_historico(args.source, args.database, args.dry_run)
    print(json.dumps(asdict(summary), ensure_ascii=False, indent=2))
    if args.dry_run:
        print("Previsualización completada; no se guardó ningún cambio.")
    else:
        print(f"Migración completada: {args.database.resolve()}")


if __name__ == "__main__":
    main()

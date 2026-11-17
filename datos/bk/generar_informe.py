from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.worksheet import Worksheet


BASE_DIR = Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR / "AFOROS DEL 2026.xlsm"
TEMPLATE_FILE = BASE_DIR / "plantilla.xlsx"

MONTHS_ES = (
    "ENERO",
    "FEBRERO",
    "MARZO",
    "ABRIL",
    "MAYO",
    "JUNIO",
    "JULIO",
    "AGOSTO",
    "SEPTIEMBRE",
    "OCTUBRE",
    "NOVIEMBRE",
    "DICIEMBRE",
)

YUMBO_DIRECT_NAMES = (
    "BSN MEDICAL",
    "LG SUPPLA CORTIJO BOD 9",
    "REFLEKTA",
    "AMCOR",
    "CERVECERIA DEL VALLE",
    "STUDIO F",
    "LITO",
    "ALDOR CARBONILLA",
)

MISION_DIRECT_NAMES = (
    "USACA ESPECIAL",
    "CARTONES AMERICA S.A.",
    "LAKE",
    "TORRES DE SANTA LUCIA",
    "CARCEL DE VILLANUEVA-CALI",
)

COMPANY_CLIENTS = {
    "JAMUNDI": ("ESPECIALES JAMUNDI", "CARTONES AMERICA - LODOS"),
    "MISION": (
        "USC ESCOMBROS",
        "CARTONES AMERICA",
        "CARTONES AMERICA - LODOS",
        "ESPECIALES MISION",
        "DIRECTA MISION",
    ),
    "YUMBO": (
        "BSN MEDICAL",
        "SUPPLA",
        "REFLEKTA",
        "AMCOR",
        "CERVECERIA DEL VALLE",
        "STUDIO F",
        "LITO",
        "ALDOR CARBONILLA",
        "ESPECIALES YUMBO",
    ),
    "BMA": ("ESPECIALES PAZIFICO",),
    "CAUCA": ("ESPECIALES CAUCA",),
    "RESTREPO": ("ESPECIALES RESTREPOLIMPIA",),
}


@dataclass(frozen=True)
class FilterClause:
    names: tuple[str, ...] = ()
    company: str | None = None
    facturable: str | None = None
    require_service_type: bool = False
    plate: str | None = None
    observation: str | None = None
    exclude_observation: str | None = None
    exclude_names: tuple[str, ...] = ()


@dataclass(frozen=True)
class ClientRule:
    label: str
    clauses: tuple[FilterClause, ...]


CLIENT_RULES = (
    ClientRule("USC ESCOMBROS", (FilterClause(names=("USACA ESPECIAL",), require_service_type=True),)),
    ClientRule(
        "CARTONES AMERICA",
        (FilterClause(names=("CARTONES AMERICA S.A.",), exclude_observation="LODOS"),),
    ),
    ClientRule(
        "CARTONES AMERICA - LODOS",
        (FilterClause(names=("CARTONES AMERICA S.A.",), observation="LODOS"),),
    ),
    ClientRule(
        "CONSTRUCTORA SOLANILLAS",
        (FilterClause(names=("LAKE",), require_service_type=True),),
    ),
    ClientRule("BSN MEDICAL", (FilterClause(names=("BSN MEDICAL",), require_service_type=True),)),
    ClientRule(
        "SUPPLA",
        (FilterClause(names=("LG SUPPLA CORTIJO BOD 9",), require_service_type=True),),
    ),
    ClientRule("REFLEKTA", (FilterClause(names=("REFLEKTA",), require_service_type=True),)),
    ClientRule("AMCOR", (FilterClause(names=("AMCOR",), require_service_type=True),)),
    ClientRule(
        "CERVECERIA DEL VALLE",
        (FilterClause(names=("CERVECERIA DEL VALLE",), require_service_type=True),),
    ),
    ClientRule("STUDIO F", (FilterClause(names=("STUDIO F",), require_service_type=True),)),
    ClientRule("LITO", (FilterClause(names=("LITO",), require_service_type=True),)),
    ClientRule(
        "ALDOR CARBONILLA",
        (FilterClause(names=("ALDOR CARBONILLA",), require_service_type=True),),
    ),
    ClientRule(
        "ESPECIALES YUMBO",
        (
            FilterClause(
                company="YUMBO LIMPIO",
                facturable="SI",
                plate="present",
                exclude_names=YUMBO_DIRECT_NAMES,
            ),
        ),
    ),
    ClientRule(
        "ESPECIALES JAMUNDI",
        (
            FilterClause(
                company="JAMUNDIASEO",
                facturable="SI",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "ESPECIALES MISION",
        (
            FilterClause(names=("TORRES DE SANTA LUCIA",), require_service_type=True),
            FilterClause(
                names=("CARCEL DE VILLANUEVA-CALI",),
                facturable="SI",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "ESPECIALES PAZIFICO",
        (
            FilterClause(
                company="BUENAVENTURA",
                facturable="SI",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "ESPECIALES CAUCA",
        (
            FilterClause(
                company="CAUCASEO",
                facturable="SI",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "ESPECIALES RESTREPOLIMPIA",
        (
            FilterClause(
                company="RESTREPOLIMPIA",
                facturable="SI",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "DIRECTA MISION",
        (
            FilterClause(
                company="MISION AMBIENTAL",
                facturable="SI",
                require_service_type=True,
                plate="present",
                exclude_names=MISION_DIRECT_NAMES,
            ),
        ),
    ),
    ClientRule(
        "CORTESIA YUMBO",
        (
            FilterClause(
                company="YUMBO LIMPIO",
                facturable="NO",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "CORTESIA JAMUNDI",
        (
            FilterClause(
                company="JAMUNDIASEO",
                facturable="NO",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "CORTESIA MISION",
        (
            FilterClause(
                company="MISION AMBIENTAL",
                facturable="NO",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "CLANDESTINO PAZIFICO",
        (
            FilterClause(
                company="BUENAVENTURA",
                facturable="NO",
                require_service_type=True,
            ),
        ),
    ),
    ClientRule(
        "CORTESIA CAUCA",
        (
            FilterClause(
                company="CAUCASEO",
                facturable="NO",
                require_service_type=True,
            ),
        ),
    ),
)


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""

    text = str(value).replace("\ufffd", "O").strip().upper()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(character for character in text if not unicodedata.combining(character))
    return " ".join(re.findall(r"[A-Z0-9]+", text))


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result.columns = [normalize_text(column).replace(" ", "_").lower() for column in result.columns]
    return result


def read_section(path: Path, sheet_name: str) -> pd.DataFrame:
    frame = pd.read_excel(path, sheet_name=sheet_name, header=1, engine="openpyxl")
    return normalize_columns(frame)


def first_client_block(frame: pd.DataFrame) -> pd.DataFrame:
    if "clientes" not in frame.columns:
        raise ValueError("No se encontró el encabezado CLIENTES.")

    client_labels = frame["clientes"].map(normalize_text)
    blank_positions = client_labels.index[client_labels.eq("")]
    end = int(blank_positions[0]) if len(blank_positions) else len(frame)
    block = frame.iloc[:end].copy()

    if block.empty:
        raise ValueError("La plantilla no contiene filas de clientes.")

    return block


def require_columns(frame: pd.DataFrame, source_name: str) -> None:
    required = {
        "fecha",
        "nombre",
        "aforo",
        "subtotal",
        "empresa",
        "tipo_servicio",
        "facturable",
        "placa",
        "observacion",
        "tarifa",
    }
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"Faltan columnas en {source_name}: {', '.join(missing)}")


def clause_mask(frame: pd.DataFrame, clause: FilterClause) -> pd.Series:
    mask = pd.Series(True, index=frame.index)

    if clause.names:
        allowed = {normalize_text(name) for name in clause.names}
        mask &= frame["nombre"].map(normalize_text).isin(allowed)

    if clause.company:
        mask &= frame["empresa"].map(normalize_text).eq(normalize_text(clause.company))

    if clause.facturable:
        mask &= frame["facturable"].map(normalize_text).eq(normalize_text(clause.facturable))

    if clause.require_service_type:
        mask &= frame["tipo_servicio"].map(normalize_text).ne("")

    if clause.plate == "present":
        mask &= frame["placa"].map(normalize_text).ne("")
    elif clause.plate == "blank":
        mask &= frame["placa"].map(normalize_text).eq("")

    if clause.observation:
        mask &= frame["observacion"].map(normalize_text).eq(normalize_text(clause.observation))

    if clause.exclude_observation:
        mask &= frame["observacion"].map(normalize_text).ne(
            normalize_text(clause.exclude_observation)
        )

    if clause.exclude_names:
        excluded = {normalize_text(name) for name in clause.exclude_names}
        mask &= ~frame["nombre"].map(normalize_text).isin(excluded)

    return mask


def rule_rows(frame: pd.DataFrame, rule: ClientRule) -> pd.DataFrame:
    mask = pd.Series(False, index=frame.index)
    for clause in rule.clauses:
        mask |= clause_mask(frame, clause)
    return frame.loc[mask]


def month_end(period: pd.Period) -> pd.Timestamp:
    return period.end_time.normalize()


def month_name(period: pd.Period) -> str:
    return MONTHS_ES[period.month - 1]


def _period_rows(frame: pd.DataFrame, period: pd.Period) -> pd.DataFrame:
    dates = pd.to_datetime(frame["fecha"], errors="coerce")
    return frame.loc[dates.dt.to_period("M").eq(period)].copy()


def _sum_numeric(values: pd.Series) -> float:
    numeric = pd.to_numeric(values, errors="coerce")
    total = numeric.sum(min_count=1)
    return 0.0 if pd.isna(total) else float(total)


def _sum_subtotal(rows: pd.DataFrame) -> float | None:
    numeric = pd.to_numeric(rows["subtotal"], errors="coerce")
    if numeric.notna().any():
        return float(numeric.sum())
    return None if not rows.empty else 0.0


def build_client_dataframe(
    production: pd.DataFrame,
    history: pd.DataFrame,
    template_block: pd.DataFrame,
    report_reference: pd.DataFrame,
    period: pd.Period,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    production = normalize_columns(production)
    history = normalize_columns(history)
    template_block = normalize_columns(template_block)
    report_reference = normalize_columns(report_reference)
    require_columns(production, "Produccion")
    require_columns(history, "Historico")

    reference_columns = {"clientes", "tarifa"}
    if not reference_columns.issubset(report_reference.columns):
        missing = sorted(reference_columns.difference(report_reference.columns))
        raise ValueError(f"Faltan columnas en Informe: {', '.join(missing)}")

    production_month = _period_rows(production, period)
    history_periods = [period - offset for offset in range(1, 4)]
    monthly_history = {item: _period_rows(history, item) for item in history_periods}

    source_rates = {
        normalize_text(row["clientes"]): row["tarifa"]
        for _, row in report_reference.iterrows()
        if normalize_text(row["clientes"])
    }

    rules_by_label = {normalize_text(rule.label): rule for rule in CLIENT_RULES}
    template_labels = template_block["clientes"].map(normalize_text)
    missing_rules = sorted(set(template_labels).difference(rules_by_label))
    if missing_rules:
        raise ValueError(f"Faltan reglas para clientes de la plantilla: {', '.join(missing_rules)}")

    missing_rates = sorted(set(template_labels).difference(source_rates))
    if missing_rates:
        raise ValueError(f"Faltan etiquetas de tarifa en la hoja Informe: {', '.join(missing_rates)}")

    output_rows: list[dict[str, object]] = []
    for _, template_row in template_block.iterrows():
        label = normalize_text(template_row["clientes"])
        rule = rules_by_label[label]
        current_rows = rule_rows(production_month, rule)

        row: dict[str, object] = {
            "CLIENTES": template_row["clientes"],
            "DESCRIPCIÓN": template_row.get("descripcion"),
            "EMPRESA": template_row.get("empresa"),
            "TARIFA": source_rates[label],
            "CANT. VIAJES": int(current_rows["aforo"].nunique(dropna=True)),
            "METROS / TON": _sum_subtotal(current_rows),
            month_name(period): _sum_numeric(current_rows["tarifa"]),
        }

        for history_period, rows in monthly_history.items():
            label_month = month_name(history_period)
            matched_rows = rule_rows(rows, rule)
            row[label_month] = _sum_numeric(matched_rows["tarifa"])

        output_rows.append(row)

    incidents = production_month.loc[production_month["subtotal"].isna()].copy()
    incident_columns = [
        column
        for column in (
            "fecha",
            "nombre",
            "aforo",
            "recipiente",
            "cantidad",
            "tipo_servicio",
            "subtotal",
        )
        if column in incidents.columns
    ]
    incidents = incidents.loc[:, incident_columns].rename(
        columns={
            "fecha": "FECHA",
            "nombre": "NOMBRE",
            "aforo": "AFORO",
            "recipiente": "RECIPIENTE",
            "cantidad": "CANTIDAD",
            "tipo_servicio": "TIPO_SERVICIO",
            "subtotal": "SUBTOTAL",
        }
    )
    return pd.DataFrame(output_rows), incidents


def build_company_dataframe(
    client_dataframe: pd.DataFrame,
    template_path: Path,
    period: pd.Period,
    rental_values: dict[str, float] | None = None,
) -> pd.DataFrame:
    template = normalize_columns(
        pd.read_excel(
            template_path,
            sheet_name="informe",
            header=49,
            engine="openpyxl",
        )
    )
    required = {"empresas"}
    if not required.issubset(template.columns):
        raise ValueError("No se encontró el encabezado EMPRESAS en el bloque de empresas.")

    client_amount_column = month_name(period)
    if client_amount_column not in client_dataframe.columns:
        raise ValueError(f"El cuadro de clientes no contiene {client_amount_column}.")

    client_values = {
        normalize_text(row["CLIENTES"]): pd.to_numeric(
            row[client_amount_column], errors="coerce"
        )
        for _, row in client_dataframe.iterrows()
    }
    rentals = {
        normalize_text(name): float(value)
        for name, value in (rental_values or {}).items()
    }

    template_companies = {
        normalize_text(company)
        for company in template["empresas"].dropna()
        if normalize_text(company) != "TOTAL"
    }
    unknown_rentals = sorted(set(rentals).difference(template_companies))
    if unknown_rentals:
        raise ValueError(
            f"Hay valores de alquiler para empresas fuera de la plantilla: "
            f"{', '.join(unknown_rentals)}"
        )

    output_rows: list[dict[str, object]] = []
    for label in template["empresas"].dropna():
        company = str(label).strip()
        normalized_company = normalize_text(company)
        if normalized_company == "TOTAL":
            break

        client_labels = COMPANY_CLIENTS.get(normalized_company)
        if client_labels is None:
            if normalized_company == "APROVECOL":
                billing = pd.NA
            else:
                raise ValueError(f"No hay regla de facturación para la empresa {company}.")
        else:
            missing_clients = [
                client
                for client in client_labels
                if normalize_text(client) not in client_values
            ]
            if missing_clients:
                raise ValueError(
                    f"Faltan filas de clientes para {company}: {', '.join(missing_clients)}"
                )
            amounts = [
                client_values[normalize_text(client)]
                for client in client_labels
            ]
            billing = pd.to_numeric(pd.Series(amounts), errors="coerce").sum(min_count=1)

        rental = rentals.get(normalized_company, pd.NA)
        difference = (
            float(billing) - float(rental)
            if not pd.isna(billing) and not pd.isna(rental)
            else pd.NA
        )
        output_rows.append(
            {
                "EMPRESAS": company,
                "FACTURACION USUARIOS": billing,
                "ALQUILER S&S": rental,
                "DIFERENCIA": difference,
            }
        )

    companies = pd.DataFrame(output_rows)
    total_billing = pd.to_numeric(companies["FACTURACION USUARIOS"], errors="coerce").sum(
        min_count=1
    )
    billable_companies = companies.loc[companies["FACTURACION USUARIOS"].notna()]
    if billable_companies["ALQUILER S&S"].notna().all():
        total_rental: object = pd.to_numeric(
            billable_companies["ALQUILER S&S"], errors="coerce"
        ).sum(min_count=1)
    else:
        total_rental = pd.NA
    total_difference = (
        float(total_billing) - float(total_rental)
        if not pd.isna(total_billing) and not pd.isna(total_rental)
        else pd.NA
    )
    return pd.concat(
        [
            companies,
            pd.DataFrame(
                [
                    {
                        "EMPRESAS": "TOTAL",
                        "FACTURACION USUARIOS": total_billing,
                        "ALQUILER S&S": total_rental,
                        "DIFERENCIA": total_difference,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )


def _available_days(
    period: pd.Period,
    through_date: pd.Timestamp | None = None,
) -> int:
    end_date = min(period.end_time.normalize(), through_date.normalize()) if through_date is not None else period.end_time.normalize()
    dates = pd.date_range(period.start_time.normalize(), end_date, freq="D")
    return int((dates.dayofweek != 6).sum())


def build_vehicle_dataframe(
    production: pd.DataFrame,
    history: pd.DataFrame,
    template_path: Path,
    period: pd.Period,
) -> pd.DataFrame:
    production = normalize_columns(production)
    history = normalize_columns(history)
    require_columns(production, "Produccion")
    require_columns(history, "Historico")

    template = normalize_columns(
        pd.read_excel(
            template_path,
            sheet_name="informe",
            header=28,
            engine="openpyxl",
        )
    )
    if "vehiculo" not in template.columns:
        raise ValueError("No se encontró el encabezado VEHICULO en la plantilla.")

    plates: list[str] = []
    for value in template["vehiculo"]:
        plate = str(value).strip() if not pd.isna(value) else ""
        if normalize_text(plate) == "TOTAL VIAJES":
            break
        if not plate:
            break
        plates.append(plate)

    if not plates:
        raise ValueError("La plantilla no contiene placas para el cuadro de vehículos.")

    production_month = _period_rows(production, period)
    latest_date = pd.to_datetime(production_month["fecha"], errors="coerce").max()
    history_periods = [period - offset for offset in range(1, 5)]
    monthly_history = {item: _period_rows(history, item) for item in history_periods}
    working_days = _available_days(
        period,
        latest_date if not pd.isna(latest_date) else None,
    )
    output_rows: list[dict[str, object]] = []

    for plate in plates:
        normalized_plate = normalize_text(plate)
        current_rows = production_month.loc[
            production_month["placa"].map(normalize_text).eq(normalized_plate)
        ]
        dates = pd.to_datetime(current_rows["fecha"], errors="coerce").dropna().dt.normalize()
        trips = int(current_rows["aforo"].nunique(dropna=True))
        favors = int(
            current_rows["nombre"].map(normalize_text).eq("FAVOR").sum()
        )

        row: dict[str, object] = {
            "VEHICULO": plate,
            "DIAS SIN OPERACIÓN": max(working_days - int(dates.nunique()), 0),
            "VIAJES REALIZADOS": trips,
            "FAVORES": favors if favors else None,
            "% TRABAJO": trips * 100 / 75,
            month_name(period): _sum_numeric(current_rows["tarifa"]),
        }

        for history_period, rows in monthly_history.items():
            plate_rows = rows.loc[rows["placa"].map(normalize_text).eq(normalized_plate)]
            row[month_name(history_period)] = _sum_numeric(plate_rows["tarifa"])

        output_rows.append(row)

    return pd.DataFrame(output_rows)


def build_minicargador_dataframe(
    template_path: Path,
    period: pd.Period,
    operating_days: dict[str, int] | None = None,
    through_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    template = normalize_columns(
        pd.read_excel(
            template_path,
            sheet_name="informe",
            header=44,
            engine="openpyxl",
        )
    )
    if "vehiculo" not in template.columns:
        raise ValueError("No se encontró el encabezado VEHICULO de minicargadores.")

    manual_days = {
        normalize_text(name): int(days)
        for name, days in (operating_days or {}).items()
    }
    available_days = _available_days(period, through_date)
    output_rows: list[dict[str, object]] = []

    for value in template["vehiculo"]:
        label = str(value).strip() if not pd.isna(value) else ""
        if not label or normalize_text(label) == "TOTAL":
            break
        normalized_label = normalize_text(label)
        days = manual_days.get(normalized_label)
        idle_days = max(available_days - days, 0) if days is not None else None
        percent = days * 100 / 25 if days is not None else None
        output_rows.append(
            {
                "VEHICULO": label,
                "DIAS SIN OPERACIÓN": idle_days,
                "DIAS DE OPERACIÓN": days,
                "% TRABAJO": percent,
            }
        )

    return pd.DataFrame(output_rows)


def build_preview(
    source_path: Path,
    template_path: Path,
    period: pd.Period,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.Timestamp | None,
    int,
]:
    production = pd.read_excel(
        source_path, sheet_name="Produccion", engine="openpyxl"
    )
    history = pd.read_excel(source_path, sheet_name="Historico", engine="openpyxl")
    template = read_section(template_path, "informe")
    report_reference = read_section(source_path, "Informe")
    template_block = first_client_block(template)
    production_normalized = normalize_columns(production)
    period_production = _period_rows(production_normalized, period)
    dates = pd.to_datetime(period_production["fecha"], errors="coerce")
    latest_date = dates.max() if not dates.empty else None

    clients, incidents = build_client_dataframe(
        production,
        history,
        template_block,
        report_reference,
        period,
    )
    companies = build_company_dataframe(clients, template_path, period)
    vehicles = build_vehicle_dataframe(production, history, template_path, period)
    minicargadores = build_minicargador_dataframe(
        template_path,
        period,
        through_date=latest_date,
    )
    return (
        clients,
        incidents,
        companies,
        vehicles,
        minicargadores,
        latest_date,
        len(period_production),
    )


def _excel_value(value: object) -> object:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _set_excel_cell(sheet: Worksheet, row: int, column: int, value: object) -> None:
    sheet.cell(row=row, column=column).value = _excel_value(value)


def export_report(
    output_path: Path,
    source_path: Path,
    template_path: Path,
    period: pd.Period,
    clients: pd.DataFrame,
    incidents: pd.DataFrame,
    companies: pd.DataFrame,
    vehicles: pd.DataFrame,
    minicargadores: pd.DataFrame,
    latest_date: pd.Timestamp | None,
) -> None:
    output_resolved = output_path.resolve()
    if output_resolved in {template_path.resolve(), source_path.resolve()}:
        raise ValueError("El archivo de salida no puede reemplazar la plantilla ni la fuente.")

    workbook = load_workbook(template_path)
    sheet = workbook["informe"]
    sheet["A1"] = period.start_time.to_pydatetime()
    sheet["A1"].number_format = "dd/mm/yyyy"

    client_months = [period - offset for offset in range(3, -1, -1)]
    vehicle_months = [period - offset for offset in range(4, -1, -1)]
    for column, month in enumerate(client_months, start=8):
        sheet.cell(row=2, column=column, value=month_name(month))
    client_lookup = {
        normalize_text(row["CLIENTES"]): row
        for _, row in clients.iterrows()
    }
    for row_number in range(3, 27):
        label = normalize_text(sheet.cell(row=row_number, column=2).value)
        data = client_lookup.get(label)
        if data is None:
            raise ValueError(f"No se encontró el cliente de la fila {row_number} en los datos.")
        for column, key in (
            (3, "DESCRIPCIÓN"),
            (4, "EMPRESA"),
            (5, "TARIFA"),
            (6, "CANT. VIAJES"),
            (7, "METROS / TON"),
        ):
            _set_excel_cell(sheet, row_number, column, data[key])
        for column, month in enumerate(client_months, start=8):
            _set_excel_cell(sheet, row_number, column, data[month_name(month)])

    vehicle_lookup = {
        normalize_text(row["VEHICULO"]): row
        for _, row in vehicles.iterrows()
    }
    for row_number in range(30, 42):
        label = normalize_text(sheet.cell(row=row_number, column=2).value)
        data = vehicle_lookup.get(label)
        if data is None:
            raise ValueError(f"No se encontró el vehículo de la fila {row_number} en los datos.")
        for column, key in (
            (3, "DIAS SIN OPERACIÓN"),
            (4, "VIAJES REALIZADOS"),
            (5, "FAVORES"),
            (6, "% TRABAJO"),
        ):
            _set_excel_cell(sheet, row_number, column, data[key])
        for column, month in enumerate(vehicle_months, start=7):
            _set_excel_cell(sheet, row_number, column, data[month_name(month)])

    for row_number, (_, data) in zip(range(46, 48), minicargadores.iterrows()):
        for column, key in (
            (3, "DIAS SIN OPERACIÓN"),
            (4, "DIAS DE OPERACIÓN"),
            (5, "% TRABAJO"),
        ):
            _set_excel_cell(sheet, row_number, column, data[key])

    company_lookup = {
        normalize_text(row["EMPRESAS"]): row
        for _, row in companies.iterrows()
        if normalize_text(row["EMPRESAS"]) != "TOTAL"
    }
    for row_number in range(51, 58):
        label = normalize_text(sheet.cell(row=row_number, column=2).value)
        data = company_lookup.get(label)
        if data is None:
            raise ValueError(f"No se encontró la empresa de la fila {row_number} en los datos.")
        _set_excel_cell(sheet, row_number, 3, data["FACTURACION USUARIOS"])
        _set_excel_cell(sheet, row_number, 4, data["ALQUILER S&S"])
        _set_excel_cell(sheet, row_number, 5, data["DIFERENCIA"])
    total = companies.loc[companies["EMPRESAS"].map(normalize_text).eq("TOTAL")].iloc[0]
    for column, key in (
        (3, "FACTURACION USUARIOS"),
        (4, "ALQUILER S&S"),
        (5, "DIFERENCIA"),
    ):
        _set_excel_cell(sheet, 58, column, total[key])

    if "Incidencias" in workbook.sheetnames:
        del workbook["Incidencias"]
    incident_sheet = workbook.create_sheet("Incidencias")
    incident_sheet.append(["Incidencias: registros con Subtotal vacío"])
    incident_sheet.append(list(incidents.columns))
    for values in incidents.itertuples(index=False, name=None):
        incident_sheet.append([_excel_value(value) for value in values])
    incident_sheet.freeze_panes = "A3"
    incident_sheet.auto_filter.ref = incident_sheet.dimensions
    incident_sheet["A1"].font = Font(bold=True, size=12)
    for cell in incident_sheet[2]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="4472C4")
    for column_cells in incident_sheet.columns:
        width = max(
            (len(str(cell.value)) for cell in column_cells if cell.value is not None),
            default=10,
        )
        incident_sheet.column_dimensions[column_cells[0].column_letter].width = min(width + 2, 34)
    for cell in incident_sheet["A"][2:]:
        if isinstance(cell.value, (pd.Timestamp,)):
            cell.number_format = "dd/mm/yyyy"

    if "Observaciones" in workbook.sheetnames:
        del workbook["Observaciones"]
    notes = workbook.create_sheet("Observaciones")
    notes.append(["Estado del informe", "Preliminar"])
    notes.append(["Periodo", str(period)])
    notes.append(
        [
            "Corte de Produccion",
            latest_date.date() if latest_date is not None else "Sin registros",
        ]
    )
    notes.append(["Alcance", "La información de octubre está incompleta; no es un cierre mensual."])
    notes.append(["Subtotal vacío", f"{len(incidents)} registros listados en la hoja Incidencias."])
    notes.append(["Alquiler S&S", "Pendiente de ingreso manual; diferencias no calculadas."])
    notes.append(["Minicargadores", "Días de operación pendientes de ingreso manual."])
    notes.append(["Candeaseo", "Cuadro pendiente de reglas y procesamiento."])
    notes.column_dimensions["A"].width = 26
    notes.column_dimensions["B"].width = 88
    for cell in notes["A"]:
        cell.font = Font(bold=True)
    for cell in notes[1]:
        cell.fill = PatternFill("solid", fgColor="FFF2CC")

    workbook.calculation.calcMode = "auto"
    workbook.calculation.fullCalcOnLoad = True
    workbook.calculation.forceFullCalc = True
    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Construye una vista previa y, opcionalmente, exporta el informe."
    )
    parser.add_argument("--source", type=Path, default=SOURCE_FILE)
    parser.add_argument("--template", type=Path, default=TEMPLATE_FILE)
    parser.add_argument("--period", default="2026-10", help="Periodo AAAA-MM.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Ruta del Excel a generar (se exporta una copia preliminar de la plantilla).",
    )
    args = parser.parse_args()

    period = pd.Period(args.period, freq="M")
    (
        clients,
        incidents,
        companies,
        vehicles,
        minicargadores,
        latest_date,
        row_count,
    ) = build_preview(
        args.source,
        args.template,
        period,
    )

    print(f"Periodo: {period}")
    print(f"Registros en Produccion: {row_count}")
    print(f"Ultima fecha disponible: {latest_date.date() if latest_date is not None else 'sin datos'}")
    if latest_date is None or latest_date < month_end(period):
        print("AVISO: el periodo no tiene datos hasta su ultimo dia; esta salida es solo una vista previa.")
    print(f"Registros con Subtotal vacio: {len(incidents)}")
    print()
    print(clients.to_string(index=False))
    print()
    print("Cuadro de empresas:")
    print(companies.to_string(index=False))
    print()
    print("Cuadro de vehículos:")
    print(vehicles.to_string(index=False))
    print()
    print("Cuadro de minicargadores (días manuales pendientes):")
    print(minicargadores.to_string(index=False))
    missing_rentals = companies.loc[
        companies["EMPRESAS"].map(normalize_text).ne("TOTAL")
        & companies["FACTURACION USUARIOS"].notna()
        & companies["ALQUILER S&S"].isna(),
        "EMPRESAS",
    ].tolist()
    if missing_rentals:
        print(f"Alquiler S&S pendiente de ingresar: {', '.join(missing_rentals)}")
    if not incidents.empty:
        print()
        print("Incidencias de Subtotal:")
        print(incidents.to_string(index=False))
    if args.output is not None:
        export_report(
            args.output,
            args.source,
            args.template,
            period,
            clients,
            incidents,
            companies,
            vehicles,
            minicargadores,
            latest_date,
        )
        print()
        print(f"Informe preliminar exportado: {args.output.resolve()}")


if __name__ == "__main__":
    main()


from pathlib import Path
from html import escape

from config import (
    PLANTILLA_CORREO,
    MES_FACTURACION,
    REMITENTE_NOMBRE
)


def construir_correo(datos):

    if not PLANTILLA_CORREO.exists():
        raise FileNotFoundError(
            f"No existe la plantilla: {PLANTILLA_CORREO}"
        )

    plantilla = PLANTILLA_CORREO.read_text(
        encoding="utf-8"
    )

    # Escapar los datos para evitar problemas con HTML
    variables = {
        "contacto": escape(datos["contacto"]),
        "nombre": escape(datos["nombre"]),
        "contrato": escape(str(datos["contrato"])),
        "metros": escape(datos["metros"]),
        "valor_t": escape(datos["valor_t"]),
        "unidad": escape(datos["unidad"]),
        "mes": escape(MES_FACTURACION),
        "aforos": escape(datos["aforos"]),
        "firma": escape(REMITENTE_NOMBRE)
    }

    # Segunda cotización opcional
    if datos["mini_activo"]:

        variables["segunda_cotizacion"] = f"""
        <p>
        Cotización: {escape(datos['mini_metros'])}
        {escape(datos['unidad'])} a ${escape(datos['valor_m'])}
        - Mes de: {escape(MES_FACTURACION)}
        
        </p>
        """

    else:
        variables["segunda_cotizacion"] = ""

    return plantilla.format(**variables)

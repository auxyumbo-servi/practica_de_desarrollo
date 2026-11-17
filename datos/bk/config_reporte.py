from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_FUENTE = BASE_DIR / "AFOROS DEL 2026.xlsm"
ARCHIVO_PLANTILLA = BASE_DIR / "plantilla.xlsx"
ARCHIVO_SALIDA = BASE_DIR / "Informe_2026-10_estructurado.xlsx"
PERIODO_REPORTE = "2026-10"
CANTIDAD_MESES_REPORTE = 4

HOJA_MES_ACTUAL = "Produccion"
HOJA_MESES_ANTERIORES = "Historico"

ETIQUETAS_COLUMNAS = {
    "fecha": "Fecha",
    "nombre": "Nombre",
    "empresa": "Empresa",
    "placa": "Placa",
    "aforo": "Aforo",
    "subtotal": "Subtotal",
    "tarifa": "Tarifa",
    "horas_alquiler": "hh-alquiler",
}

CLIENTES_INCLUIDOS = (
    "USC ESCOMBROS",
    "CARTONES AMERICA",
    "CARTONES AMERICA - LODOS",
    "CONSTRUCTORA SOLANILLAS",
    "BSN MEDICAL",
    "SUPPLA",
    "REFLEKTA",
    "AMCOR",
    "CERVECERIA DEL VALLE",
    "STUDIO F",
    "LITO",
    "ALDOR CARBONILLA",
)

ETIQUETAS_CUADROS = {
    "clientes": "CLIENTES",
    "empresas": "EMPRESAS",
    "vehiculos": "VEHICULO",
    "alquileres": "ALQUILERES",
}

HOJAS_REPORTE = {
    "clientes": "Clientes",
    "empresas": "Empresas",
    "vehiculos": "Vehiculos",
    "alquileres": "Alquileres",
}

TABLAS_EXCEL = {
    "clientes": "TablaClientes",
    "empresas": "TablaEmpresas",
    "vehiculos": "TablaVehiculos",
    "alquileres": "TablaAlquileres",
}

PLACAS_VEHICULOS = (
    "UQX887",
    "JAV293",
    "JWF334",
    "TTG575",
    "SIS902",
    "TAV095",
    "CER549",
    "VDA722",
    "BLB557",
    "VCM251",
    "JAV292",
    "QFO978",
)

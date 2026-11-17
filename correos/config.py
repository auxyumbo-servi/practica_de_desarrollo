from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_TIME, "es_CO.UTF-8")

#mes a trabajar
mes_anterior = (datetime.now() - relativedelta(months=1)).strftime("%B").upper()


# Rutas del proyecto
RUTA_EXCEL = Path("C:/Users/PRODUCCION/OneDrive/Desktop/TRABAJO DE PRODUCCION/")
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
MODULES_DIR = BASE_DIR / "modules"
TEMPLATES_DIR = BASE_DIR / "templates"
LOGS_DIR = BASE_DIR / "logs"

# Excel
ARCHIVO_EXCEL = RUTA_EXCEL / "AFOROS DEL 2026.xlsm"
HOJA_EXCEL = "correo"

# Facturación

MES_FACTURACION = (
    (datetime.now() - relativedelta(months=1))
    .strftime("%B")
    .upper()
)

REMITENTE_NOMBRE = "Natalia Hernandez"
DESTINARIO_NOMBRE = "Patricia Bravo"

# Outlook
MODO_ENVIO = "BORRADOR"

# Opciones: BORRADOR o ENVIAR

# =====================================
# CONFIGURACIÓN DE CORREOS
# =====================================

CUENTA_REMITENTE = "auxproduccion@servintegrales.com.co"

# Destinatarios fijos
DESTINATARIOS_FIJOS = [
    "auxiliarfacturacion@servintegrales.com.co",
]

# Copias fijas
COPIAS_FIJAS = [
    "facturacion@servintegrales.com.co",
    "asalazar@servintegrales.com.co", 
    "samaya@servintegrales.com.co"  
]

# Utilizar también los destinatarios del Excel
USAR_CORREO_EXCEL = True
USAR_COPIA_EXCEL = True


# Plantilla
PLANTILLA_CORREO = TEMPLATES_DIR / "correo.html"

# Columnas requeridas
COLUMNAS_REQUERIDAS = [
    "Nombre",
    "MiniMetros",
    "Metros",
    "Contrato",
    "ValorT",
    "ValorM",
    "Unidad",
    "Aforos",
    "Asunto",
    "Contacto",
    "Correo",
    "Archivo",
    "Copia"
]

COLUMNAS = [
    "Nombre",
    "Contrato",
    "Subtotal",
    "Recipiente",
    "aforo",
    

]


# Crear carpetas si no existen
for carpeta in [DATA_DIR, LOGS_DIR]:
    carpeta.mkdir(parents=True, exist_ok=True)


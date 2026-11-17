import pandas as pd


#ruta archivo
ruta_archivo = r"C:\Users\PRODUCCION\OneDrive\Desktop\TRABAJO DE PRODUCCION\py\datos\AFOROS DEL 2026.xlsm"


# Leer el archivo de Excel
def leer_archivo_excel(ruta_archivo, hoja):
    try:
        df = pd.read_excel(
            ruta_archivo,
            sheet_name=hoja,
            engine="openpyxl"
        )
        return df
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

users =[
    "BSN MEDICAL",
    "USACA"
]
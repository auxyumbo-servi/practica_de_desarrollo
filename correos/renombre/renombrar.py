import os
import pandas as pd
import re
import datetime
import sqlite3

from config import RUTA_EXCEL, BASE_DIR

def renombrar():

    def definir_fecha_actual():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def mes_anterior():
        hoy = datetime.datetime.now()
        primer_dia_mes_actual = datetime.datetime(hoy.year, hoy.month, 1)
        ultimo_dia_mes_anterior = primer_dia_mes_actual - datetime.timedelta(days=1)

        meses = [
            "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
        ]

        return meses[ultimo_dia_mes_anterior.month - 1]

    RUTA = RUTA_EXCEL / "ESPECIALES YUMBO"
    BASE = BASE_DIR
    # Carpeta donde están los PDFs
    carpeta_pdfs = os.path.join(RUTA, mes_anterior())

    #ARCHIVO SQL
    #archivo_sql = os.path.join(BASE, "lista.db")
    MAX_LEN = 200  # longitud máxima del nombre del archivo

    # Archivo Excel en otra carpeta
    archivo_excel = os.path.join(BASE, "lista.xlsx")

    def limpiar_y_acortar(nombre):
        nombre = re.sub(r'[\\/:*?"<>|]', '_', nombre).strip()
        if len(nombre) > MAX_LEN:
            nombre = nombre[:MAX_LEN]
        return nombre

    #conexion = sqlite3.connect(archivo_sql)

    #df = pd.read_sql_query("SELECT * FROM lista", conexion)
    df = pd.read_excel(archivo_excel)
    #conexion.close()



    if not {"Antiguo", "Nuevo"}.issubset(df.columns):
        raise ValueError("El Excel debe tener columnas 'Antiguo' y 'Nuevo' exactamente.")

    # Obtener archivos PDF existentes
    archivos_pdf = {
        os.path.splitext(f)[0].strip().upper(): f
        for f in os.listdir(carpeta_pdfs)
        if f.lower().endswith(".pdf")
    }

    for _, fila in df.iterrows():
        nombre_antiguo = str(fila["Antiguo"]).strip().upper()
        nombre_nuevo = str(fila["Nuevo"]).strip()

        archivo_real = archivos_pdf.get(nombre_antiguo)

        if archivo_real:
            ruta_antigua = os.path.join(carpeta_pdfs, archivo_real)

            nombre_final = limpiar_y_acortar(nombre_nuevo).upper()
            ruta_nueva = os.path.join(carpeta_pdfs, nombre_final + ".pdf")

            if os.path.exists(ruta_nueva):
                print(f"⚠️ Ya existe el destino: {nombre_final}.pdf")
                continue

            os.rename(ruta_antigua, ruta_nueva)

            print(f"✅ {archivo_real} → {nombre_final}.pdf")

        else:
            print(f"⚠️ No encontrado: {nombre_antiguo}")

    print("Renombrado completado ✅")
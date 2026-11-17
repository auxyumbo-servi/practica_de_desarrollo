import os
import pandas as pd
import datetime
import sqlite3

from config import RUTA_EXCEL, BASE_DIR

def listar():
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

    mes = mes_anterior()
    DIR_BASE = BASE_DIR
    RUTA = RUTA_EXCEL / "ESPECIALES YUMBO"
    archivo_salida = carpeta_pdfs = os.path.join(DIR_BASE, "lista.xlsx") # archivo Excel de salida, se concatena con la ruta
    #archivo_salida = carpeta_pdfs = os.path.join(DIR_BASE, "lista.db") # archivo sqLite de salida, se concatena con la ruta
    carpeta_pdfs = os.path.join(RUTA, mes) # carpeta donde están los PDFs, se concatena con el mes

    # Excel de donde tomar los nuevos nombres
    archivo_nuevos = RUTA_EXCEL / "AFOROS DEL 2026.xlsm"
    hoja_nuevos = "correo"
    columna_nuevos = "Asunto"


    # ==========================
    # LEER PDFs
    # ==========================

    def obtener_nombres_pdfs(ruta_carpeta):
        return [
            os.path.splitext(f)[0].upper()
            for f in os.listdir(ruta_carpeta)
            if f.lower().endswith(".pdf")
        ]

    nombres_pdfs = obtener_nombres_pdfs(carpeta_pdfs)


    # ==========================
    # ORDENAR ANTIGUOS
    # ==========================

    nombres_pdfs = sorted(nombres_pdfs)  # orden ascendente por Antiguo

    # ==========================
    # LEER NUEVOS NOMBRES
    # ==========================

    df_nuevos = pd.read_excel(archivo_nuevos, sheet_name=hoja_nuevos)
    lista_nuevos = df_nuevos[columna_nuevos].astype(str).tolist()

    # Si hay menos nuevos que PDFs, rellenar con vacío
    while len(lista_nuevos) < len(nombres_pdfs):
        lista_nuevos.append("")

    # ==========================
    # ORDENAR NUEVOS
    # ==========================

    lista_nuevos = sorted(
    lista_nuevos[:len(nombres_pdfs)],
    key=lambda x: str(x)
)  # orden ascendente por Nuevo

    # ==========================
    # CREAR DATAFRAME FINAL
    # ==========================

    df = pd.DataFrame({
        "Antiguo": nombres_pdfs[:len(lista_nuevos)],  # se mantiene lista de PDFs
        "Nuevo": lista_nuevos
    })

    # ==========================
    # GUARDAR EN EXCEL
    # ==========================
    
    df.to_excel(archivo_salida, index=False)
    #df.to_sql("lista", sqlite3.connect(archivo_salida), index=False, if_exists="replace")

    print("Proceso terminado")
    print(f"Total de PDFs encontrados: {len(nombres_pdfs)}")
    print(f"Archivo Excel creado: {archivo_salida}")

    if os.path.exists(archivo_salida):
        print(f"Archivo Excel creado en: {archivo_salida}")


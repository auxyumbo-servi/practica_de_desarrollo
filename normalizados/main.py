import pandas as pd
import re
import unicodedata
from rapidfuzz import process, fuzz

ARCHIVO = "ajuste.xlsx"

UMBRAL = 90

# --------------------------
# NORMALIZACION
# --------------------------

def normalizar(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto).upper()

    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

    texto = re.sub(r'\bS\.?A\.?S\.?\b', '', texto)
    texto = re.sub(r'\bLTDA\b', '', texto)
    texto = re.sub(r'\bLIMITADA\b', '', texto)
    texto = re.sub(r'\bS\.?A\.?\b', '', texto)

    texto = re.sub(r'[^A-Z0-9 ]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)

    return texto.strip()

# --------------------------
# LEER EXCEL
# --------------------------

df_orig = pd.read_excel(
    ARCHIVO,
    sheet_name="originales"
)

df_trat = pd.read_excel(
    ARCHIVO,
    sheet_name="tratados"
)

# --------------------------
# NORMALIZAR
# --------------------------

df_orig["NOMBRE_NORM"] = df_orig["NOMBRE"].apply(normalizar)
df_trat["NOMBRE_NORM"] = df_trat["NOMBRE"].apply(normalizar)

nombres_tratados = df_trat["NOMBRE_NORM"].tolist()

# --------------------------
# BUSCAR COINCIDENCIAS
# --------------------------

coincidencias = []
solo_originales = []
dudosos = []

usados_tratados = set()

for _, fila in df_orig.iterrows():

    mejor = process.extractOne(
        fila["NOMBRE_NORM"],
        nombres_tratados,
        scorer=fuzz.token_sort_ratio
    )

    if mejor is None:
        solo_originales.append(fila)
        continue

    nombre_match, score, indice = mejor

    registro_tratado = df_trat.iloc[indice]

    nombre_real_tratado = registro_tratado["NOMBRE"]
    idusuario_tratado = registro_tratado["idusuario"]

    if score >= UMBRAL:

        usados_tratados.add(indice)

        coincidencias.append({
            "idusuario_original": fila["idusuario"],
            "nombre_original": fila["NOMBRE"],

            "idusuario_tratado": idusuario_tratado,
            "nombre_tratado": nombre_real_tratado,

            "similitud": round(score, 2),
            "nombre_oficial": fila["NOMBRE"]
        })

    elif score >= 70:

        dudosos.append({
            "idusuario_original": fila["idusuario"],
            "nombre_original": fila["NOMBRE"],

            "idusuario_tratado": idusuario_tratado,
            "mejor_match": nombre_real_tratado,

            "similitud": round(score, 2)
        })

    else:
        solo_originales.append(fila)
# --------------------------
# SOLO TRATADOS
# --------------------------

solo_tratados = df_trat.drop(index=list(usados_tratados))

# --------------------------
# EXPORTAR
# --------------------------

with pd.ExcelWriter(
    "resultado_normalizacion.xlsx",
    engine="openpyxl"
) as writer:

    pd.DataFrame(coincidencias).to_excel(
        writer,
        sheet_name="Coincidencias",
        index=False
    )

    pd.DataFrame(dudosos).to_excel(
        writer,
        sheet_name="Dudosos",
        index=False
    )

    pd.DataFrame(solo_originales).to_excel(
        writer,
        sheet_name="Solo_Originales",
        index=False
    )

    solo_tratados.to_excel(
        writer,
        sheet_name="Solo_Tratados",
        index=False
    )

print("Proceso finalizado")
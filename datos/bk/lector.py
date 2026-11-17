import pandas as pd
from config import ruta_archivo, leer_archivo_excel, users

hoja = "Produccion"


df = leer_archivo_excel(ruta_archivo, hoja)

df = df.rename(columns={"Subtotal": "Cantidad","Cantidad": "Metros"})
df = df.loc[df["Tipo_servicio"] .notnull(),["Nombre", "Cantidad", "Tarifa"]]


def suma_subtotal(df):
    subtotal = df.groupby("Nombre")["Cantidad"].sum()
    return subtotal

def suma_tarifa(df):
    total = df.groupby("Nombre")["Tarifa"].sum()
    return total


def suma_total(df):
    total = df.groupby("Nombre")[["Cantidad", "Tarifa"]].sum()
    return total

def suma_user(df, users):
    resultados = {}

    for user in users:
        total = df.loc[
            df["Nombre"].eq(user),
            ["Cantidad", "Tarifa"]
        ].sum()

        resultados[user] = total

        print(f"\n{user} {total["Cantidad"]},{total["Tarifa"]}")

# Verificar los encabezados y los primeros registros
#print(df.columns.tolist())
#print(df)
#print(suma_total(df))
suma_user(df,users)
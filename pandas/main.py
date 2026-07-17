from db import obtener_datos
from transformar import transformar
from reglas_cliente import aplicar_reglas_clientes
from prueba import exportar_meses_desde_columnas


df = obtener_datos()
df = transformar(df)
df = aplicar_reglas_clientes(df)

exportar_meses_desde_columnas(df, columna_cliente="CLIENTES")

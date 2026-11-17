from config import ruta_archivo, leer_archivo_excel

hoja = "tarifas"

#Variables del DataFrame (df)
nombre = "Nombre"
tarifa = "Tarifa"
tipo_servicio = "Tipo_servicio"

def usuarios():
    df = leer_archivo_excel(ruta_archivo,"tarifas")
    df = df.loc[df[nombre].notnull(),['Nombre','Empresa',]]
    df = df.dropna(axis=1, how="all")
    print(df.columns.tolist())

    print(df.head(2))

usuarios()


def tarifas():
    df = leer_archivo_excel(ruta_archivo,"tarifas")
    df = df.loc[df[nombre].notnull(),['Nombre', 'Tipo_servicio', 'Recipiente', 'Tarifa', 'Vigencia_Desde', 'Vigencia_Hasta', 'Facturable', 'Minicargador2', 'Empresa', 'Minicargador', 'Correo']]
    df = df.dropna(axis=1, how="all")
    #print(df.columns.tolist())
    print(df.head(2))

#tarifas()
#df = df.loc[df[nombre].notnull(),[nombre,]]



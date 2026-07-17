def normalizar_cliente(nombre):
    """
    Convierte nombres de BD a nombres estándar del Excel
    """
    nombre = str(nombre).strip().upper()

    mapa = {
    "USC ESCOMBROS" : "USACA ESPECIAL" ,
    "CARTONES AMERICA" : "CARTONES AMERICA S.A" ,
    "CONSTRUCTORA SOLANILLAS" : "LAKE" ,
    "BSN MEDICAL" : "BSN MEDICAL" ,
    "SUPPLA" : "LG SUPPLA CORTIJO BOD 9" ,
    "REFLEKTA" : "REFLEKTA" ,
    "AMCOR" : "AMCOR" ,
    "CERVECERIA DEL VALLE" : "CERVECERIA DEL VALLE" ,
    "STUDIO F" : "STUDIO F" ,
    "LITO" : "LITO" ,
    "ALDOR CARBONILLA" : "ALDOR CARBONILLA" 

    }

    return mapa.get(nombre, nombre)
import datetime
from dataclasses import dataclass

@dataclass
class Fecha:
    dia: int
    mes: int
    año: int
    completa: str

def fecha_anterior():
    hoy = datetime.datetime.now()
    ultimo_dia = hoy.replace(day=1) - datetime.timedelta(days=1)

    return Fecha(
        dia=ultimo_dia.day,
        mes=ultimo_dia.month,
        año=ultimo_dia.year,
        completa=ultimo_dia.strftime("%d/%m/%Y")
    )
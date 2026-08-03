from sqlalchemy.orm import Mapped

from models.base import BaseModel


class Recipiente(BaseModel):

    __tablename__ = "recipientes"


    nombre: Mapped[str]


    precio: Mapped[float]


    cantidad_disponible: Mapped[int]
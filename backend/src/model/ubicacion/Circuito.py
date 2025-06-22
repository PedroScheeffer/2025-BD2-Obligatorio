from typing import Optional
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity

class CircuitoSchema(BaseModel):
    id: Optional[int]
    accesibilidad: bool
    id_establecimiento: int
    id_zona: int
    id_eleccion: int
    id_tipo_eleccion: int


class Circuito(BaseEntity):
    table_name = "CIRCUITO"
    values_needed = [
        "id",
        "accesibilidad",
        "id_establecimiento",
        "id_zona",
        "id_eleccion",
        "id_tipo_eleccion"
    ]

    def __init__(self, id: Optional[int], accesibilidad: bool, id_establecimiento: int, id_zona: int, id_eleccion: int, id_tipo_eleccion: int):
        self.id = id
        self.accesibilidad = accesibilidad
        self.id_establecimiento = id_establecimiento
        self.id_zona = id_zona
        self.id_eleccion = id_eleccion
        self.id_tipo_eleccion = id_tipo_eleccion
from typing import Optional
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel
from model.BaseEntity import BaseEntity
from model.schemas.Direccion import DireccionSchema
from model.ubicacion.Zona import ZonaSchema


class EstablecimientoSchema(BaseModel):
    id: Optional[int]
    tipo: str
    direccion: DireccionSchema
    id_zona: int


class Establecimiento(BaseEntity):
    table_name = "ESTABLECIMIENTO"
    values_needed = ["id", "tipo", "direccion", "id_zona"]

    def __init__(self, id: Optional[int], tipo: str, direccion, id_zona: int):
        self.id = id
        self.tipo = tipo
        self.direccion = direccion
        self.id_zona = id_zona

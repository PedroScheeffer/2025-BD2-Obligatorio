from typing import Optional
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity


class ZonaSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID de la zona")
    paraje: str = Field(..., description="Paraje de la zona")
    ciudad: str
    departamento: str
    municipio: str


class Zona(BaseEntity):
    table_name = "ZONA"
    values_needed = ["id", "paraje", "ciudad", "departamento", "municipio"]

    def __init__(self, id: int, paraje: str, ciudad: str, departamento: str, municipio: str):
        self.id = id
        self.paraje = paraje
        self.ciudad = ciudad
        self.departamento = departamento
        self.municipio = municipio

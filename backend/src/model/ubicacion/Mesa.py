from typing import Optional
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel
from model.BaseEntity import BaseEntity


class MesaSchema(BaseModel):
    id: Optional[int]
    id_circuito: int
    cc_vocal: str
    cc_secretario: str
    cc_presidente: str


class Mesa(BaseEntity):
    table_name = "MESA"
    values_needed = [
        "id",
        "id_circuito",
        "cc_vocal",
        "cc_secretario",
        "cc_presidente"
    ]

    def __init__(self, id: int, id_circuito: int, cc_vocal: str, cc_secretario: str, cc_presidente: str):
        self.id = id
        self.id_circuito = id_circuito
        self.cc_vocal = cc_vocal
        self.cc_secretario = cc_secretario
        self.cc_presidente = cc_presidente


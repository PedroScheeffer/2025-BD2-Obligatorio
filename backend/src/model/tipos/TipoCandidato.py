from typing import Optional
from pydantic import BaseModel
from model.BaseEntity import BaseEntity
from enum import Enum


class TipoCandidatoEnum(str, Enum):
    presidente = "presidente"
    vicepresidente = "vicepresidente"
    senador = "senador"
    alcalde = "alcalde"


class TipoCandidatoSchema(BaseModel):
    id: Optional[int]
    tipo: str


class TipoCandidato(BaseEntity):
    def __init__(self, id: Optional[int], tipo: str):
        self.id = id
        self.tipo = tipo

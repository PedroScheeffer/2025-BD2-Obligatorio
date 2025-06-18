from typing import Optional
from pydantic import BaseModel
from model.BaseEntity import BaseEntity
from enum import Enum


class TipoEleccionEnum(str, Enum):
    presidencial = "presidencial"
    ballotage = "ballotage"
    municipales = "municipales"
    plebiscito = "plebiscito"
    referendum = "referéndum"


class TipoEleccionSchema(BaseModel):
    id: Optional[int]
    tipo: str


class TipoEleccion(BaseEntity):
    def __init__(self, id: Optional[int], tipo: str):
        self.id = id
        self.tipo = tipo

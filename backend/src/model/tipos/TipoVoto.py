from typing import Optional
from pydantic import BaseModel
from model.BaseEntity import BaseEntity
from enum import Enum


class TipoVotoEnum(str, Enum):
    valido = "valido"
    anulado = "anulado"
    blanco = "blanco"


class TipoVotoSchema(BaseModel):
    id: Optional[int]
    tipo: str


class TipoVoto(BaseEntity):
    def __init__(self, id: Optional[int], tipo: str):
        self.id = id
        self.tipo = tipo

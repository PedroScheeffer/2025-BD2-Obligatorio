from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity


class CandidatoListaSchema(BaseModel):
    cc: str = Field(..., description="Credencial cívica de la persona")
    valor_lista: int = Field(..., description="Valor de la lista")
    id_partido: int = Field(..., description="ID del partido")
    id_eleccion: int = Field(..., description="ID de la elección")


class CandidatoLista(BaseEntity):
    table_name = "CANDIDATO_LISTA"
    values_needed = ["cc", "valor_lista",
                     "id_partido", "id_eleccion", ]
    primary_key = "cc"  # O una tupla para clave compuesta si lo deseas

    def __init__(self, cc: str, valor_lista: int, id_partido: int, id_eleccion: int):
        self.cc = cc
        self.valor_lista = valor_lista
        self.id_partido = id_partido
        self.id_eleccion = id_eleccion

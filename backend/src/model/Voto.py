from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity


class VotoSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID del voto")
    valor_lista: int = Field(..., description="Valor de la lista")
    id_partido: int = Field(..., description="ID del partido")
    id_eleccion: int = Field(..., description="ID de la elección")
    es_observado: bool = Field(..., description="¿Es observado?")
    id_tipo_voto: int = Field(..., description="ID del tipo de voto")
    id_circuito: int = Field(..., description="ID del circuito")
    fecha: str = Field(..., description="Fecha del voto (YYYY-MM-DD)")


class Voto(BaseEntity):
    table_name = "VOTO"
    values_needed = ["id", "valor_lista", "id_partido", "id_eleccion",
                     "id_tipo_eleccion", "es_observado", "id_tipo_voto", "id_circuito", "fecha"]
    primary_key = "id"

    def __init__(self, id: int | None, valor_lista: int, id_partido: int, id_eleccion: int,  es_observado: bool, id_tipo_voto: int, id_circuito: int, fecha: str):
        self.id = id
        self.valor_lista = valor_lista
        self.id_partido = id_partido
        self.id_eleccion = id_eleccion
        self.es_observado = es_observado
        self.id_tipo_voto = id_tipo_voto
        self.id_circuito = id_circuito
        self.fecha = fecha  # Store as string in YYYY-MM-DD format

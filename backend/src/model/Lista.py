from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity


class ListaSchema(BaseModel):
    valor: int = Field(..., description="Valor de la lista")
    id_partido: int = Field(..., description="ID del partido")
    id_eleccion: int = Field(..., description="ID de la elección")



class Lista(BaseEntity):
    table_name = "LISTA"
    values_needed = ["valor", "id_partido", "id_eleccion"]
    primary_key = "valor"  # Puede requerir clave compuesta

    def __init__(self, valor: int, id_partido: int, id_eleccion: int):
        self.valor = valor
        self.id_partido = id_partido
        self.id_eleccion = id_eleccion


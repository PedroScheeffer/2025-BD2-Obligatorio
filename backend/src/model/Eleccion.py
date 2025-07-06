from typing import Optional, List
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity
from model.ubicacion.Circuito import CircuitoSchema


class EleccionSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID de la elección")
    fecha: str = Field(..., description="Fecha de la elección (YYYY-MM-DD)")
    id_tipo_eleccion: int = Field(..., description="ID del tipo de elección")


class EleccionConCircuitosSchema(EleccionSchema):
    circuitos: List[CircuitoSchema] = []


class Eleccion(BaseEntity):
    table_name = "ELECCION"
    values_needed = ["id", "fecha", "id_tipo_eleccion"]
    primary_key = "id"

    def __init__(self, id: int | None, fecha: str, id_tipo_eleccion: int):
        self.id = id
        self.fecha = fecha  # Store as string in YYYY-MM-DD format
        self.id_tipo_eleccion = id_tipo_eleccion

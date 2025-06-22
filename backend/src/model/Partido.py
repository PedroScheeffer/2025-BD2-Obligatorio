from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity


class PartidoSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID del partido")
    nombre: str = Field(..., description="Nombre del partido")
    direccion_sede: dict = Field(...,
                                 description="Dirección de la sede (JSON)")


class Partido(BaseEntity):
    table_name = "PARTIDO"
    values_needed = ["id", "nombre", "direccion_sede"]
    primary_key = "id"

    def __init__(self, id: int, nombre: str, direccion_sede: str):
        self.id = id
        self.nombre = nombre
        self.direccion_sede = direccion_sede  # Store as JSON string

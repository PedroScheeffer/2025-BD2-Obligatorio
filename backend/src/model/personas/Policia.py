from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity
from model.personas.Persona import Persona


class PoliciaSchema(BaseModel):
    cc_persona: str = Field(..., description="Credencial cívica de la persona")
    comisaria: str = Field(..., description="Comisaría")
    fk_id_establecimiento: int = Field(...,
                                       description="ID del establecimiento")
    fk_id_zona: int = Field(..., description="ID de la zona")


class Policia(Persona):
    table_name = "POLICIA"
    values_needed = ["cc_persona", "comisaria",
                     "fk_id_establecimiento", "fk_id_zona"]
    primary_key = "cc_persona"

    def __init__(self, cc_persona: str, comisaria: str, fk_id_establecimiento: int, fk_id_zona: int, cc: str = None, ci: int = None, nombre: str = None, fecha_nacimiento: str = None):
        super().__init__(cc=cc, ci=ci, nombre=nombre, fecha_nacimiento=fecha_nacimiento)
        self.cc_persona = cc_persona
        self.comisaria = comisaria
        self.fk_id_establecimiento = fk_id_establecimiento
        self.fk_id_zona = fk_id_zona

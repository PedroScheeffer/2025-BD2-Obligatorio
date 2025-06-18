from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity
from model.personas.Persona import Persona


class CandidatoSchema(BaseModel):
    cc_persona: str = Field(..., description="Credencial cívica de la persona")
    id_tipo: int = Field(..., description="ID del tipo de candidato")


class Candidato(Persona):
    table_name = "CANDIDATO"
    values_needed = ["cc_persona", "id_tipo"]
    primary_key = "cc_persona"

    def __init__(self, cc_persona: str, id_tipo: int, cc: str = None, ci: int = None, nombre: str = None, fecha_nacimiento: str = None):
        super().__init__(cc=cc, ci=ci, nombre=nombre, fecha_nacimiento=fecha_nacimiento)
        self.cc_persona = cc_persona
        self.id_tipo = id_tipo

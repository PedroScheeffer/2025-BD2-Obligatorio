from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity
from model.personas.Persona import Persona, PersonaSchema


class VocalSchema(PersonaSchema):
    cc_persona: str = Field(..., description="Credencial cívica de la persona")


class Vocal(Persona):
    table_name = "VOCAL"
    values_needed = ["cc_persona"]
    primary_key = "cc_persona"

    def __init__(self, cc_persona: str, cc: str = None, ci: int = None, nombre: str = None, fecha_nacimiento: str = None):
        super().__init__(cc=cc, ci=ci, nombre=nombre, fecha_nacimiento=fecha_nacimiento)
        self.cc_persona = cc_persona

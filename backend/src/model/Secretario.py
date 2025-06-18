from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity
from model.personas.Persona import Persona


class SecretarioSchema(BaseModel):
    cc_persona: str = Field(..., description="Credencial cívica de la persona")


class Secretario(Persona, BaseEntity):
    table_name = "SECRETARIO"
    values_needed = ["cc_persona"]
    primary_key = "cc_persona"

    def __init__(self, cc_persona: str, cc: str = None, ci: int = None, nombre: str = None, fecha_nacimiento: str = None):
        super().__init__(cc=cc, ci=ci, nombre=nombre, fecha_nacimiento=fecha_nacimiento)
        self.cc_persona = cc_persona

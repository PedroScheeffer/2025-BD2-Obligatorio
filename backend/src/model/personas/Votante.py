from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity
from model.personas.Persona import Persona


class VotanteSchema(BaseModel):
    cc_persona: str = Field(..., description="Credencial cívica de la persona")
    voto: bool = Field(..., description="¿Votó?")
    id_circuito: int = Field(..., description="ID del circuito")


class Votante(Persona):
    table_name = "VOTANTE"
    values_needed = ["cc_persona", "voto", "id_circuito"]
    primary_key = "cc_persona"

    def __init__(self, cc_persona: str, voto: bool, id_circuito: int, cc: str = None, ci: int = None, nombre: str = None, fecha_nacimiento: str = None):
        super().__init__(cc=cc, ci=ci, nombre=nombre, fecha_nacimiento=fecha_nacimiento)
        self.cc_persona = cc_persona
        self.voto = voto
        self.id_circuito = id_circuito

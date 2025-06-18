from pydantic import  Field
from model.personas.Persona import Persona, PersonaSchema


class CandidatoSchema(PersonaSchema):
    cc_persona: str 
    id_tipo: int 


class Candidato(Persona):
    table_name = "CANDIDATO"
    values_needed = ["cc_persona", "id_tipo"]
    primary_key = "cc_persona"

    def __init__(self, cc_persona: str, id_tipo: int, cc: str = None, ci: int = None, nombre: str = None, fecha_nacimiento: str = None):
        super().__init__(cc=cc, ci=ci, nombre=nombre, fecha_nacimiento=fecha_nacimiento)
        self.cc_persona = cc_persona
        self.id_tipo = id_tipo

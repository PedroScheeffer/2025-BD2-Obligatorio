from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel, Field, field_validator
from model.BaseEntity import BaseEntity


class PersonaSchema(BaseModel):
    cc: str = Field(..., description="Credencial Civica ej ABC 1234")
    ci: int = Field(..., description="Cédula de Identidad ej 12345678")
    nombre: str = Field(..., description="Nombre completo de la persona")
    fecha_nacimiento: str = Field(...,
                                  description="Fecha de nacimiento en formato YYYY-MM-DD")

    @field_validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, value):
        from datetime import date
        if isinstance(value, str):
            # Parse the string to validate it's a valid date
            try:
                date_obj = date.fromisoformat(value)
                if date_obj > date.today():
                    raise ValueError("Fecha de nacimiento no puede ser futura")
            except ValueError as e:
                raise ValueError(f"Fecha inválida: {e}")
        return value


class Persona(BaseEntity):
    table_name = "PERSONA"
    values_needed = ["cc", "ci", "nombre", "fecha_nacimiento"]
    primary_key = "cc"
    
    def __init__(self, cc: str, ci: int, nombre: str, fecha_nacimiento: str):
        self.cc = cc
        self.ci = ci
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento

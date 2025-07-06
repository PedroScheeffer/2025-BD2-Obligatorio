from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel, Field, field_validator
from model.BaseEntity import BaseEntity
from datetime import date
from typing import Union


class PersonaSchema(BaseModel):
    cc: str = Field(..., description="Credencial Civica ej ABC 1234")
    ci: int = Field(..., description="Cédula de Identidad ej 12345678")
    nombre: str = Field(..., description="Nombre completo de la persona")
    fecha_nacimiento: str | date = Field(...,
                                  description="Fecha de nacimiento en formato YYYY-MM-DD")
    contrasena: str | None = Field("1234", description="Contraseña de la persona")

    @field_validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, value):
        if isinstance(value, date):
            if value > date.today():
                raise ValueError("Fecha de nacimiento no puede ser futura")
            return value.isoformat()
        if isinstance(value, str):
            try:
                value = date.fromisoformat(value)
            except ValueError as e:
                raise ValueError(f"Fecha inválida: {e}")

        if value > date.today():
            raise ValueError("Fecha de nacimiento no puede ser futura")
        return value.isoformat()


class Persona(BaseEntity):
    table_name = "PERSONA"
    values_needed = ["cc", "ci", "nombre", "fecha_nacimiento", "contrasena"]
    primary_key = "cc"

    def __init__(self, cc: str, ci: int, nombre: str, fecha_nacimiento: str, contrasena: str | None = "1234"):
        self.cc = cc
        self.ci = ci
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.contrasena = contrasena


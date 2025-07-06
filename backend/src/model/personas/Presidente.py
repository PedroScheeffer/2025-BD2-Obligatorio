from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity
from model.personas.Persona import Persona, PersonaSchema
from config.logger import logger
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner


class PresidenteSchema(PersonaSchema):
    cc: str = Field(..., description="Credencial cívica de la persona")


class Presidente(Persona):
    table_name = "PRESIDENTE"
    values_needed = ["cc"]
    primary_key = "cc"

    def __init__(self, cc: str, ci: int, nombre: str, fecha_nacimiento: str, contrasena: str | None = "1234", **kwargs):
        # Initialize the parent Persona class with all its required attributes
        super().__init__(cc=cc, ci=ci, nombre=nombre,
                         fecha_nacimiento=fecha_nacimiento, contrasena=contrasena)

    def insert(self):
        """
        Custom insert method for Presidente.
        Inserts only the specific fields (cc) into the PRESIDENTE table.
        """
        try:
            script = f"INSERT INTO {self.table_name} (cc) VALUES (%s)"
            params = (self.cc,)

            inserted_id = MySQLScriptRunner.run_insert_script_and_get_id(
                script=script, params=params
            )

            if inserted_id is not None:
                logger.info(
                    f"Successfully inserted entity into {self.table_name} with cc {self.cc}")
                return self
            return None
        except Exception as e:
            logger.error(f"Error inserting into {self.table_name}: {e}")
            return None

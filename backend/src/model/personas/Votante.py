from typing import Optional, Union
from pydantic import BaseModel, Field
from model.personas.Persona import Persona, PersonaSchema
from datetime import date
from config.logger import logger
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner


class VotanteSchema(PersonaSchema):
    voto: bool = Field(..., description="¿Votó?")
    id_circuito: int = Field(..., description="ID del circuito")


class Votante(Persona):
    table_name = "VOTANTE"
    values_needed = ["cc", "voto", "id_circuito"]
    primary_key = "cc"

    def __init__(self, cc: str, ci: int, nombre: str, fecha_nacimiento: str, voto: bool, id_circuito: int, contrasena: str | None = "1234", **kwargs):
        # Initialize the parent Persona class with all its required attributes
        super().__init__(cc=cc, ci=ci, nombre=nombre,
                         fecha_nacimiento=fecha_nacimiento, contrasena=contrasena)
        # Set the specific attributes for the Votante
        self.voto = voto
        self.id_circuito = id_circuito

    def insert(self):
        """
        Custom insert method for Votante.
        Inserts only the specific fields (cc, voto, id_circuito) into the VOTANTE table.
        """
        try:
            script = f"INSERT INTO {self.table_name} (cc, voto, id_circuito) VALUES (%s, %s, %s)"
            params = (self.cc, self.voto, self.id_circuito)

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

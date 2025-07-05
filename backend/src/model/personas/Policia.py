from typing import Optional
from pydantic import BaseModel, Field
from model.BaseEntity import BaseEntity
from model.personas.Persona import Persona, PersonaSchema
from config.logger import logger
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner


class PoliciaSchema(PersonaSchema):
    comisaria: str = Field(..., description="Comisaría")
    fk_id_establecimiento: int = Field(...,
                                       description="ID del establecimiento")


class Policia(Persona):
    table_name = "POLICIA"
    values_needed = ["cc", "comisaria",
                     "fk_id_establecimiento", "fk_id_zona"]
    primary_key = "cc"

    def __init__(self, cc: str, ci: int, nombre: str, fecha_nacimiento: str, comisaria: str, fk_id_establecimiento: int, fk_id_zona: int, contrasena: str | None = "1234", **kwargs):
        super().__init__(cc=cc, ci=ci, nombre=nombre,
                         fecha_nacimiento=fecha_nacimiento, contrasena=contrasena)
        self.comisaria = comisaria
        self.fk_id_establecimiento = fk_id_establecimiento

    def insert(self):
        """
        Custom insert method for Policia.
        Inserts only the specific fields into the POLICIA table.
        """
        try:
            script = f"INSERT INTO {self.table_name} (cc, comisaria, fk_id_establecimiento) VALUES (%s, %s, %s)"
            params = (self.cc, self.comisaria,
                      self.fk_id_establecimiento)

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

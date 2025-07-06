from config.logger import logger
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from model.personas.Persona import Persona, PersonaSchema


class FuncionarioSchema(PersonaSchema):
    pass


class Funcionario(Persona):
    table_name = "FUNCIONARIO"
    primary_key = "cc"

    def __init__(self, cc: str, ci: int, nombre: str, fecha_nacimiento: str, **kwargs):
        super().__init__(cc=cc, ci=ci, nombre=nombre,
                         fecha_nacimiento=fecha_nacimiento, **kwargs)

    def insert(self):
        """
        Custom insert method for Funcionario.
        Inserts the Persona data first, then inserts the cc into the FUNCIONARIO table.
        """
        try:
            # First, insert the Persona data by calling the parent's insert method
            super().insert()
        except Exception as e:
            # If the error is a duplicate key, it means the Persona already exists.
            # This is expected if we are creating a Funcionario from an existing Persona.
            if "Duplicate entry" in str(e):
                logger.warning(f"Persona {self.cc} already exists. Proceeding to ensure Funcionario record.")
            else:
                # For other errors, we should log and re-raise
                logger.error(f"Error inserting Persona data for {self.cc}: {e}")
                raise e

        try:
            # Now, insert into the Funcionario table
            script = f"INSERT INTO {self.table_name} (cc) VALUES (%s)"
            params = (self.cc,)

            MySQLScriptRunner.run_insert_script_and_get_id(
                script=script, params=params
            )
            logger.info(
                f"Successfully inserted/verified entity in {self.table_name} with cc {self.cc}")
            return self

        except Exception as e:
            # If the Funcionario already exists, we can consider it a success.
            if "Duplicate entry" in str(e):
                logger.warning(f"Funcionario {self.cc} already exists in {self.table_name}.")
                return self
            
            logger.error(f"Error inserting into {self.table_name}: {e}")
            return None

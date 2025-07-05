from config.logger import logger 
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from model.personas.Persona import Persona, PersonaSchema


class CandidatoSchema(PersonaSchema):
    cc: str
    id_tipo: int


class Candidato(Persona):
    table_name = "CANDIDATO"
    values_needed = ["cc", "id_tipo"]
    primary_key = "cc"


    def __init__(self, cc: str, ci: int, nombre: str, fecha_nacimiento: str, id_tipo: int, contrasena: str | None = "1234", **kwargs):
        super().__init__(cc=cc, ci=ci, nombre=nombre,
                         fecha_nacimiento=fecha_nacimiento, contrasena=contrasena)
        self.id_tipo = id_tipo

    def insert(self):
        """
        Custom insert method for Candidato.
        Inserts only the specific fields (cc, id_tipo) into the CANDIDATO table.
        """
        try:
            # The script is specific to the CANDIDATO table structure
            script = f"INSERT INTO {self.table_name} (cc, id_tipo) VALUES (%s, %s)"
            params = (self.cc, self.id_tipo)
            
            # Use the script runner to execute the custom query
            inserted_id = MySQLScriptRunner.run_insert_script_and_get_id(
                script=script, params=params
            )
            
            if inserted_id is not None:
                logger.info(f"Successfully inserted entity into {self.table_name} with cc {self.cc}")
                return self
            return None
        except Exception as e:
            logger.error(f"Error inserting into {self.table_name}: {e}")
            return None
from datetime import date
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel, Field, field_validator

class PersonaSchema(BaseModel):
    cc: str = Field(..., description="Credencial Civica ej ABC 1234")
    ci: int = Field(..., description="Cédula de Identidad ej 12345678")
    nombre: str = Field(..., description="Nombre completo de la persona")
    fecha_nacimiento: date = Field(..., description="Fecha de nacimiento en formato YYYY-MM-DD")
    
    @field_validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, value):
        if isinstance(value, str):
            value = date.fromisoformat(value)
        if value > date.today():
            raise ValueError("Fecha de nacimiento no puede ser futura")
        return value
    

class Persona:
    table_name = "PERSONA"
    values_needed = ["cc", "ci", "nombre", "fecha_nacimiento"]

    def __init__(self, cc: str, ci: int, nombre: str, fecha_nacimiento: str):
        self.cc = cc
        self.ci = ci
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento


    def insert(self) -> bool:
        try:
            script, params = Querier.create_insert_script(
                entity=self,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(script=script, params=params)
            return status 
        except Exception as e:
            print(f"Error inserting Persona: {e}")
            return False
    

    def update(self) -> bool:
        try:
            script, params = Querier.create_update_script(
                entity=self,
                filter_key="cc",
                filter_value=self.cc,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(script=script, params=params)
            return status
        except Exception as e:
            print(f"Error updating Persona: {e}")
            return False
        

    def delete(self) -> bool:
        try:
            script, params = Querier.create_delete_script(
                filter_key="cc",
                filter_value=self.cc,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(script=script, params=params)
            return status
        except Exception as e:
            print(f"Error deleting Persona: {e}")
            return False
        

    def get_persona(cc: str) -> dict:
        try:
            script, params = Querier.create_select_all_columns_script(
                filter_key="cc",
                filter_value=cc,
                table_name=Persona.table_name
            )
            result = MySQLScriptRunner.run_script_to_query_database(script=script, params=params)
            if result:
                return DataFormatter.format_dict(result[0])
            else:
                raise ValueError(f"No record found for cc: {cc}")
        except Exception as e:
            print(f"Error retrieving Persona with cc {cc}: {e}")
            raise e
        

    def get_all_personas() -> list[dict]:
        try:
            script = f"SELECT * FROM {Persona.table_name}"
            result = MySQLScriptRunner.run_script_to_query_database(script=script)
            return [DataFormatter.format_dict(row) for row in result]
        except Exception as e:
            print(f"Error retrieving all Personas: {e}")
            raise e

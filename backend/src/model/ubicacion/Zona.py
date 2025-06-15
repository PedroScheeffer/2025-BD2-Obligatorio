from typing import Optional
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel, Field

class ZonaSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID de la zona")
    paraje: str = Field(..., description="Paraje de la zona")
    ciudad: str
    departamento: str
    municipio: str


class Zona:
    table_name = "ZONA"
    values_needed = ["id", "paraje", "ciudad", "departamento", "municipio"]

    def __init__(self, id: Optional[int], paraje: str, ciudad: str, departamento: str, municipio: str):
        self.id = id
        self.paraje = paraje
        self.ciudad = ciudad
        self.departamento = departamento
        self.municipio = municipio

    def insert(self) -> bool:
        try:
            script, params = Querier.create_insert_script(
                entity=self,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(script=script, params=params)
            return status 
        except Exception as e:
            print(f"Error inserting Zona: {e}")
            return False
    

    def update(self) -> bool:
        try:
            script, params = Querier.create_update_script(
                entity=self,
                filter_key="id",
                filter_value=self.id,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(script=script, params=params)
            return status
        except Exception as e:
            print(f"Error updating Zona: {e}")
            return False
    

    def delete(self) -> bool:
        try:
            script, params = Querier.create_delete_script(
                filter_key="id",
                filter_value=self.id,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(script=script, params=params)
            return status
        except Exception as e:
            print(f"Error deleting Zona: {e}")
            return False
        
    
    def get_entity(self, id: int) -> Optional[dict]:
        try:
            script, params = Querier.create_select_all_columns_script(
                filter_key="id",
                filter_value=id,
                table_name=self.table_name
            )
            result = MySQLScriptRunner.run_script_to_query_database(script=script, params=params)
            if result:
                return DataFormatter.format_dict(result[0])
            return None
        except Exception as e:
            print(f"Error getting Zona: {e}")
            return None
        
    def get_all_zonas(self) -> list:
        try:
            script, params = Querier.create_select_all_columns_script(
                table_name=self.table_name
            )
            result = MySQLScriptRunner.run_script_to_query_database(script=script, params=params)
            if result:
                return [DataFormatter.format_dict(row) for row in result]
            return []
        except Exception as e:
            print(f"Error getting all Zonas: {e}")
            return []
from typing import Optional
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel

from model.schemas.Direccion import DireccionSchema
from model.ubicacion.Zona import ZonaSchema


class EstablecimientoSchema(BaseModel):
    id: Optional[int]
    tipo: str
    direccion: DireccionSchema
    zona: ZonaSchema


class Establecimiento:
    table_name = "ESTABLECIMIENTO"
    values_needed = ["id", "tipo", "direccion", "zona"]

    def __init__(self, id: Optional[int], tipo: str, direccion: DireccionSchema, zona: ZonaSchema):
        self.id = id
        self.tipo = tipo
        self.direccion = direccion
        self.zona = zona

    def insert(self) -> bool:
        try:
            script, params = Querier.create_insert_script(
                entity=self,
                table_name=self.table_name
            )
            status = MySQLScriptRunner.run_script_to_modify_database(
                script=script, params=params)
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
            status = MySQLScriptRunner.run_script_to_modify_database(
                script=script, params=params)
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
            status = MySQLScriptRunner.run_script_to_modify_database(
                script=script, params=params)
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
            result = MySQLScriptRunner.run_script_to_query_database(
                script=script, params=params)
            if result:
                return DataFormatter.format_dict(result[0])
            return None
        except Exception as e:
            print(f"Error getting Zona: {e}")
            return None

    def get_all_establecimento() -> list[dict]:
        try:
            script = f"SELECT * FROM {Establecimiento.table_name}"
            result = MySQLScriptRunner.run_script_to_query_database(
                script=script)
            return [DataFormatter.format_dict(row) for row in result]
        except Exception as e:
            print(f"Error retrieving all establecimiento: {e}")
            raise e

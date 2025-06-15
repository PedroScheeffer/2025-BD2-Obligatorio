from typing import Optional
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from utils.DataFormatter import DataFormatter
from pydantic import BaseModel, Field


class CircuitoSchema(BaseModel):
    id: Optional[int]
    accesibilidad: bool
    id_establecimiento: int
    id_zona: int
    id_eleccion: int
    id_tipo_eleccion: int


class Circuito(BaseModel):
    table_name = "CIRCUITO"
    values_needed = [
        "id",
        "accesibilidad",
        "id_establecimiento",
        "id_zona",
        "id_eleccion",
        "id_tipo_eleccion"
    ]

    def __init__(self, id: Optional[int], accesibilidad: bool, id_establecimiento: int, id_zona: int, id_eleccion: int, id_tipo_eleccion: int):
        self.id = id
        self.accesibilidad = accesibilidad
        self.id_establecimiento = id_establecimiento
        self.id_zona = id_zona
        self.id_eleccion = id_eleccion
        self.id_tipo_eleccion = id_tipo_eleccion

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

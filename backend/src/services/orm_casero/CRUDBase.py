from typing import Optional, List, Dict, Any, Type

from annotated_types import T
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator as Querier
from config.logger import logger


class CRUDBase:
    """
    Generico clase con op CRUD para manejar entidades en una base de datos MySQL.
    """

    def __init__(self, model_class: T, table_name: str, primary_key: str = "id"):
        self.model_class = model_class
        self.table_name = table_name
        self.primary_key = primary_key

    def insert(self, entity: T) -> T | None:
        try:
            logger.debug(f"Inserting entity into {self.table_name}")
            script, params = Querier.create_insert_script(
                entity=entity,
                table_name=self.table_name
            )
            inserted_id = MySQLScriptRunner.run_insert_script_and_get_id(
                script=script, params=params
            )
            if inserted_id is not None:
                # Update the entity's ID with the database-generated ID
                if hasattr(entity, 'id'):
                    entity.id = inserted_id
                logger.info(
                    f"Successfully inserted entity into {self.table_name} with ID {inserted_id}")
                return entity
            return None
        except Exception as e:
            logger.error(f"Error inserting {self.table_name}: {e}")
            return entity

    def update(self, entity: T, filter_value: Any) -> T | None:
        try:
            logger.debug(
                f"Updating entity in {self.table_name} with {self.primary_key}={filter_value}")
            script, params = Querier.create_update_script(
                entity=entity,
                filter_key=self.primary_key,
                filter_value=filter_value,
                table_name=self.table_name
            )
            result = MySQLScriptRunner.run_script_to_modify_database(
                script=script, params=params
            )  
            if result:
                logger.info(
                    f"Successfully updated entity in {self.table_name} with {self.primary_key}={filter_value}")
                result = entity.crud().get_by_id(entity.filter_value)
            return result
        except Exception as e:
            logger.error(f"Error updating {self.table_name}: {e}")
            return None

    def delete(self, filter_value: Any) -> bool:
        try:
            logger.debug(
                f"Deleting entity from {self.table_name} with {self.primary_key}={filter_value}")
            script, params = Querier.create_delete_script(
                filter_key=self.primary_key,
                filter_value=filter_value,
                table_name=self.table_name
            )
            result = MySQLScriptRunner.run_script_to_modify_database(
                script=script, params=params
            )
            if result:
                logger.info(
                    f"Successfully deleted entity from {self.table_name} with {self.primary_key}={filter_value}")
            return result
        except Exception as e:
            logger.error(f"Error deleting {self.table_name}: {e}")
            return False

    def get_by_id(self, id_value: Any) -> T | None:
        try:
            logger.debug(
                f"Getting entity from {self.table_name} with {self.primary_key}={id_value}")
            script, params = Querier.create_select_all_columns_script(
                filter_key=self.primary_key,
                filter_value=id_value,
                table_name=self.table_name
            )
            result = MySQLScriptRunner.run_script_to_query_database(
                script=script, params=params
            )
            if result:
                logger.debug(
                    f"Found entity in {self.table_name} with {self.primary_key}={id_value}")
                entity = self.model_class(**result)
                return entity
            logger.debug(
                f"No entity found in {self.table_name} with {self.primary_key}={id_value}")
            return None
        except Exception as e:
            logger.error(f"Error getting {self.table_name}: {e}")
            return None

    def get_by_field(self, field_name: str, field_value: Any) -> Optional[T]:
        try:
            logger.debug(
                f"Getting entity from {self.table_name} with {field_name}={field_value}")
            script, params = Querier.create_select_all_columns_script(
                filter_key=field_name,
                filter_value=field_value,
                table_name=self.table_name
            )
            result = MySQLScriptRunner.run_script_to_query_database(
                script=script, params=params
            )
            if result:
                logger.debug(
                    f"Found entity in {self.table_name} with {field_name}={field_value}")
                return self.model_class(**result)
            logger.debug(
                f"No entity found in {self.table_name} with {field_name}={field_value}")
            return None
        except Exception as e:
            logger.error(
                f"Error getting {self.table_name} by {field_name}: {e}")
            return None

    def get_all(self) -> List[T]:
        try:
            logger.debug(f"Getting all entities from {self.table_name}")
            script = f"SELECT * FROM {self.table_name}"
            result = MySQLScriptRunner.run_script_to_query_database(
                script=script)
            if result:
                logger.debug(
                    f"Retrieved {len(result)} entities from {self.table_name}")
                return [self.model_class(**row) for row in result]
            logger.debug(f"No entities found in {self.table_name}")
            return []
        except Exception as e:
            logger.error(f"Error getting all {self.table_name}: {e}")
            return []

    def get_multiple_by_field(self, field_name: str, field_value: Any) -> List[T]:
        try:
            logger.debug(
                f"Getting multiple entities from {self.table_name} with {field_name}={field_value}")
            script, params = Querier.create_select_all_columns_script(
                filter_key=field_name,
                filter_value=field_value,
                table_name=self.table_name
            )
            result = MySQLScriptRunner.run_script_to_query_database(
                script=script, params=params
            )
            if result:
                logger.debug(
                    f"Found {len(result)} entities in {self.table_name} with {field_name}={field_value}")
                return [self.model_class(**row) for row in result]
            logger.debug(
                f"No entities found in {self.table_name} with {field_name}={field_value}")
            return []
        except Exception as e:
            logger.error(
                f"Error getting {self.table_name} by {field_name}: {e}")
            return []

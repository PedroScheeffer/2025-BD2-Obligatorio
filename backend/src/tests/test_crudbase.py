import unittest
from model.BaseEntity import BaseEntity
from services.orm_casero.CRUDBase import CRUDBase
from unittest.mock import patch, MagicMock

# Dummy entity for testing


class DummyEntity(BaseEntity):
    table_name = "DUMMY"
    values_needed = ["id", "name"]
    primary_key = "id"

    def __init__(self, id, name):
        self.id = id
        self.name = name


class TestCRUDBase(unittest.TestCase):
    def setUp(self):
        self.entity = DummyEntity(id=1, name="Test")
        self.crud = DummyEntity.crud()

    @patch("services.orm_casero.MySQLScriptRunner.run_script_to_modify_database", return_value=True)
    @patch("services.orm_casero.MySQLScriptGenerator.create_insert_script", return_value=("INSERT ...", {}))
    def test_insert(self, mock_script, mock_runner):
        result = self.crud.insert(self.entity)
        self.assertTrue(result)
        mock_script.assert_called_once()
        mock_runner.assert_called_once()

    @patch("services.orm_casero.MySQLScriptRunner.run_script_to_modify_database", return_value=True)
    @patch("services.orm_casero.MySQLScriptGenerator.create_update_script", return_value=("UPDATE ...", {}))
    def test_update(self, mock_script, mock_runner):
        result = self.crud.update(self.entity, filter_value=1)
        self.assertTrue(result)
        mock_script.assert_called_once()
        mock_runner.assert_called_once()

    @patch("services.orm_casero.MySQLScriptRunner.run_script_to_modify_database", return_value=True)
    @patch("services.orm_casero.MySQLScriptGenerator.create_delete_script", return_value=("DELETE ...", {}))
    def test_delete(self, mock_script, mock_runner):
        result = self.crud.delete(filter_value=1)
        self.assertTrue(result)
        mock_script.assert_called_once()
        mock_runner.assert_called_once()

    @patch("services.orm_casero.MySQLScriptRunner.run_script_to_query_database", return_value=[{"id": 1, "name": "Test"}])
    @patch("services.orm_casero.MySQLScriptGenerator.create_select_all_columns_script", return_value=("SELECT ...", {}))
    @patch("utils.DataFormatter.format_dict", return_value={"id": 1, "name": "Test"})
    def test_get_by_id(self, mock_format, mock_script, mock_runner):
        result = self.crud.get_by_id(1)
        self.assertEqual(result, {"id": 1, "name": "Test"})
        mock_script.assert_called_once()
        mock_runner.assert_called_once()
        mock_format.assert_called_once()

    @patch("services.orm_casero.MySQLScriptRunner.run_script_to_query_database", return_value=[{"id": 1, "name": "Test"}])
    def test_get_all(self, mock_runner):
        result = self.crud.get_all()
        self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()

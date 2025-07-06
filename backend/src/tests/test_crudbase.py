import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Ensure backend/src is in sys.path for absolute imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))

from services.orm_casero.CRUDBase import CRUDBase
from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
from services.orm_casero.MySQLScriptGenerator import MySQLScriptGenerator
from typing import Optional


from model.BaseEntity import BaseEntity

class MockEntity(BaseEntity):
    """Mock entity class for testing"""
    def __init__(self, id: Optional[int] = None, name: str = "", email: str = ""):
        self.id = id
        self.name = name
        self.email = email
    
    def __eq__(self, other):
        if not isinstance(other, MockEntity):
            return False
        return self.id == other.id and self.name == other.name and self.email == other.email


class TestCRUDBase:
    """Test suite for CRUDBase class"""
    
    @pytest.fixture
    def crud_instance(self):
        """Create a CRUDBase instance for testing"""
        return CRUDBase(MockEntity, "test_table", "id")
    
    @pytest.fixture
    def mock_entity(self):
        """Create a mock entity for testing"""
        return MockEntity(id=1, name="Test User", email="test@example.com")
    
    @pytest.fixture
    def mock_entity_no_id(self):
        """Create a mock entity without ID for insert testing"""
        return MockEntity(name="New User", email="new@example.com")

    # INSERT TESTS
    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_insert_script_and_get_id')
    @patch('services.orm_casero.CRUDBase.Querier.create_insert_script')
    def test_insert_success(self, mock_create_insert, mock_run_insert, crud_instance, mock_entity_no_id):
        """Test successful entity insertion"""
        # Arrange
        mock_create_insert.return_value = ("INSERT INTO test_table...", ["param1", "param2"])
        mock_run_insert.return_value = 123
        
        # Act
        result = crud_instance.insert(mock_entity_no_id)
        
        # Assert
        assert result is not None
        assert result.id == 123
        assert result.name == "New User"
        assert result.email == "new@example.com"
        mock_create_insert.assert_called_once_with(entity=mock_entity_no_id, table_name="test_table")
        mock_run_insert.assert_called_once_with(script="INSERT INTO test_table...", params=["param1", "param2"])

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_insert_script_and_get_id')
    @patch('services.orm_casero.CRUDBase.Querier.create_insert_script')
    def test_insert_failure(self, mock_create_insert, mock_run_insert, crud_instance, mock_entity_no_id):
        """Test failed entity insertion"""
        # Arrange
        mock_create_insert.return_value = ("INSERT INTO test_table...", ["param1", "param2"])
        mock_run_insert.return_value = None
        
        # Act
        result = crud_instance.insert(mock_entity_no_id)
        
        # Assert
        assert result is None

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_insert_script_and_get_id')
    @patch('services.orm_casero.CRUDBase.Querier.create_insert_script')
    def test_insert_exception(self, mock_create_insert, mock_run_insert, crud_instance, mock_entity_no_id):
        """Test exception handling during insertion"""
        # Arrange
        mock_create_insert.side_effect = Exception("Database error")
        
        # Act
        result = crud_instance.insert(mock_entity_no_id)
        
        # Assert
        assert result == mock_entity_no_id  # Returns original entity on exception

    # UPDATE TESTS
    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_modify_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_update_script')
    def test_update_success(self, mock_create_update, mock_run_modify, crud_instance, mock_entity):
        """Test successful entity update"""
        # Arrange
        mock_create_update.return_value = ("UPDATE test_table...", ["param1", "param2"])
        mock_run_modify.return_value = True
        
        # Mock the T.crud().get_by_id call that's problematic
        with patch.object(crud_instance, 'get_by_id', return_value=mock_entity):
            # Act
            result = crud_instance.update(mock_entity, 1)
        
        # Assert
        assert result == mock_entity
        mock_create_update.assert_called_once_with(
            entity=mock_entity, 
            filter_key="id", 
            filter_value=1, 
            table_name="test_table"
        )
        mock_run_modify.assert_called_once_with(script="UPDATE test_table...", params=["param1", "param2"])

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_modify_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_update_script')
    def test_update_failure(self, mock_create_update, mock_run_modify, crud_instance, mock_entity):
        """Test failed entity update"""
        # Arrange
        mock_create_update.return_value = ("UPDATE test_table...", ["param1", "param2"])
        mock_run_modify.return_value = False
        
        # Act
        result = crud_instance.update(mock_entity, 1)
        
        # Assert
        assert result is False

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_modify_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_update_script')
    def test_update_exception(self, mock_create_update, mock_run_modify, crud_instance, mock_entity):
        """Test exception handling during update"""
        # Arrange
        mock_create_update.side_effect = Exception("Database error")
        
        # Act
        result = crud_instance.update(mock_entity, 1)
        
        # Assert
        assert result is None

    # DELETE TESTS
    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_modify_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_delete_script')
    def test_delete_success(self, mock_create_delete, mock_run_modify, crud_instance):
        """Test successful entity deletion"""
        # Arrange
        mock_create_delete.return_value = ("DELETE FROM test_table...", ["param1"])
        mock_run_modify.return_value = True
        
        # Act
        result = crud_instance.delete(1)
        
        # Assert
        assert result is True
        mock_create_delete.assert_called_once_with(
            filter_key="id", 
            filter_value=1, 
            table_name="test_table"
        )
        mock_run_modify.assert_called_once_with(script="DELETE FROM test_table...", params=["param1"])

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_modify_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_delete_script')
    def test_delete_failure(self, mock_create_delete, mock_run_modify, crud_instance):
        """Test failed entity deletion"""
        # Arrange
        mock_create_delete.return_value = ("DELETE FROM test_table...", ["param1"])
        mock_run_modify.return_value = False
        
        # Act
        result = crud_instance.delete(1)
        
        # Assert
        assert result is False

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_modify_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_delete_script')
    def test_delete_exception(self, mock_create_delete, mock_run_modify, crud_instance):
        """Test exception handling during deletion"""
        # Arrange
        mock_create_delete.side_effect = Exception("Database error")
        
        # Act
        result = crud_instance.delete(1)
        
        # Assert
        assert result is False

    # GET BY ID TESTS
    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_select_all_columns_script')
    def test_get_by_id_success(self, mock_create_select, mock_run_query, crud_instance):
        """Test successful get by ID"""
        # Arrange
        mock_create_select.return_value = ("SELECT * FROM test_table...", ["param1"])
        mock_run_query.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}
        
        # Act
        result = crud_instance.get_by_id(1)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.name == "Test User"
        assert result.email == "test@example.com"
        mock_create_select.assert_called_once_with(
            filter_key="id", 
            filter_value=1, 
            table_name="test_table"
        )

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_select_all_columns_script')
    def test_get_by_id_not_found(self, mock_create_select, mock_run_query, crud_instance):
        """Test get by ID when entity not found"""
        # Arrange
        mock_create_select.return_value = ("SELECT * FROM test_table...", ["param1"])
        mock_run_query.return_value = None
        
        # Act
        result = crud_instance.get_by_id(999)
        
        # Assert
        assert result is None

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_select_all_columns_script')
    def test_get_by_id_exception(self, mock_create_select, mock_run_query, crud_instance):
        """Test exception handling during get by ID"""
        # Arrange
        mock_create_select.side_effect = Exception("Database error")
        
        # Act
        result = crud_instance.get_by_id(1)
        
        # Assert
        assert result is None

    # GET BY FIELD TESTS
    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_select_all_columns_script')
    def test_get_by_field_success(self, mock_create_select, mock_run_query, crud_instance):
        """Test successful get by field"""
        # Arrange
        mock_create_select.return_value = ("SELECT * FROM test_table...", ["param1"])
        mock_run_query.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}
        
        # Act
        result = crud_instance.get_by_field("email", "test@example.com")
        
        # Assert
        assert result is not None
        assert result.email == "test@example.com"
        mock_create_select.assert_called_once_with(
            filter_key="email", 
            filter_value="test@example.com", 
            table_name="test_table"
        )

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_select_all_columns_script')
    def test_get_by_field_not_found(self, mock_create_select, mock_run_query, crud_instance):
        """Test get by field when entity not found"""
        # Arrange
        mock_create_select.return_value = ("SELECT * FROM test_table...", ["param1"])
        mock_run_query.return_value = None
        
        # Act
        result = crud_instance.get_by_field("email", "nonexistent@example.com")
        
        # Assert  
        assert result is None

    # GET ALL TESTS
    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    def test_get_all_success(self, mock_run_query, crud_instance):
        """Test successful get all entities"""
        # Arrange
        mock_run_query.return_value = [
            {"id": 1, "name": "User 1", "email": "user1@example.com"},
            {"id": 2, "name": "User 2", "email": "user2@example.com"}
        ]
        
        # Act
        result = crud_instance.get_all()
        
        # Assert
        assert len(result) == 2
        assert result[0].id == 1
        assert result[0].name == "User 1"
        assert result[1].id == 2
        assert result[1].name == "User 2"
        mock_run_query.assert_called_once_with(script="SELECT * FROM test_table")

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    def test_get_all_empty(self, mock_run_query, crud_instance):
        """Test get all when no entities exist"""
        # Arrange
        mock_run_query.return_value = None
        
        # Act
        result = crud_instance.get_all()
        
        # Assert
        assert result == []

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    def test_get_all_exception(self, mock_run_query, crud_instance):
        """Test exception handling during get all"""
        # Arrange
        mock_run_query.side_effect = Exception("Database error")
        
        # Act
        result = crud_instance.get_all()
        
        # Assert
        assert result == []

    # GET MULTIPLE BY FIELD TESTS
    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_select_all_columns_script')
    def test_get_multiple_by_field_success(self, mock_create_select, mock_run_query, crud_instance):
        """Test successful get multiple by field"""
        # Arrange
        mock_create_select.return_value = ("SELECT * FROM test_table...", ["param1"])
        mock_run_query.return_value = [
            {"id": 1, "name": "Test User 1", "email": "test1@example.com"},
            {"id": 2, "name": "Test User 2", "email": "test2@example.com"}
        ]
        
        # Act
        result = crud_instance.get_multiple_by_field("name", "Test%")
        
        # Assert
        assert len(result) == 2
        assert result[0].name == "Test User 1"
        assert result[1].name == "Test User 2"
        mock_create_select.assert_called_once_with(
            filter_key="name", 
            filter_value="Test%", 
            table_name="test_table"
        )

    @patch('services.orm_casero.CRUDBase.MySQLScriptRunner.run_script_to_query_database')
    @patch('services.orm_casero.CRUDBase.Querier.create_select_all_columns_script')
    def test_get_multiple_by_field_empty(self, mock_create_select, mock_run_query, crud_instance):
        """Test get multiple by field when no entities found"""
        # Arrange
        mock_create_select.return_value = ("SELECT * FROM test_table...", ["param1"])
        mock_run_query.return_value = None
        
        # Act
        result = crud_instance.get_multiple_by_field("status", "inactive")
        
        # Assert
        assert result == []

    # INITIALIZATION TESTS
    def test_crud_initialization(self):
        """Test CRUDBase initialization"""
        # Act
        crud = CRUDBase(MockEntity, "users", "user_id")
        
        # Assert
        assert crud.model_class == MockEntity
        assert crud.table_name == "users"
        assert crud.primary_key == "user_id"

    def test_crud_initialization_default_primary_key(self):
        """Test CRUDBase initialization with default primary key"""
        # Act
        crud = CRUDBase(MockEntity, "users")
        
        # Assert
        assert crud.model_class == MockEntity
        assert crud.table_name == "users"
        assert crud.primary_key == "id"  # Default value


if __name__ == "__main__":
    pytest.main([__file__])

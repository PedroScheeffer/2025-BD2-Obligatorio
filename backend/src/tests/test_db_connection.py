from services.orm_casero.MySQLScriptRunner import MySQLScriptRunner
import pytest
from dotenv import load_dotenv
import sys
import os
# Ensure backend/src is in sys.path for absolute imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))

# Load test environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


def test_db_connection():
    """Test if database connection can be established"""
    print("DB environment variables:")
    print(f"DB_HOST: {os.environ.get('DB_HOST')}")
    print(f"DB_PORT: {os.environ.get('DB_PORT')}")
    print(f"DB_USER: {os.environ.get('DB_USER')}")
    print(f"DB_PASSWORD: {os.environ.get('DB_PASSWORD')}")
    print(f"DB_NAME: {os.environ.get('DB_NAME')}")

    # Try a simple query to test connection
    try:
        result = MySQLScriptRunner.run_script_to_query_database(
            "SELECT 1 as test", ())
        print(f"DB connection test result: {result}")
        assert result is not None
    except Exception as e:
        print(f"DB connection failed: {e}")
        pytest.fail(f"Database connection failed: {e}")


if __name__ == "__main__":
    test_db_connection()

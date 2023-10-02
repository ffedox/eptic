import sys
import pytest
sys.path.append("../src")  # Append the source directory to the system path

from db_connect import connect_to_db, get_database_config_from_json

@pytest.fixture(scope="module")
def db_config():
    return get_database_config_from_json("../config.json")

@pytest.fixture(scope="module")
def db_connection(db_config):
    connection = connect_to_db(db_config)
    yield connection
    connection.close()

def test_connect_to_db(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT DISTINCT lang FROM texts")
    unique_langs = [row[0] for row in cursor.fetchall()]
    assert unique_langs, "Unable to fetch unique languages."

    cursor.close()

if __name__ == "__main__":
    pytest.main()

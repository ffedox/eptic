import mariadb
import json
from omegaconf import DictConfig
import hydra
import pytest

def get_database_config_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return data["database"]

def connect_to_db(config_data):
    conn = mariadb.connect(
        user=config_data['user'],
        password=config_data['password'],
        host=config_data['host'],
        port=config_data['port'],
        database=config_data['name']
    )
    return conn

@hydra.main(config_path="../config", config_name="main", version_base=None)
def main(config: DictConfig):
    # Run the tests
    pytest.main(["-x", config.paths.tests])

    # Use Hydra to get the path to config.json and then get the database config from it
    print(f"Processing data using {config.db.credentials}")

    config_data = get_database_config_from_json(config.db.credentials)

    # Get the database connection
    conn = connect_to_db(config_data)
    
    # Ensure to close the connection after use.
    conn.close()

if __name__ == "__main__":
    main()
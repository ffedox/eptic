import mariadb
import json
from omegaconf import DictConfig
import hydra

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

    config_data = get_database_config_from_json(config.db.credentials)

    print(f"Connecting to database: {config_data['name']}")

    # Get the database connection
    conn = connect_to_db(config_data)
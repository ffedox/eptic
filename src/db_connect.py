import mariadb
import json
from omegaconf import DictConfig
import hydra
import pandas as pd
from sqlalchemy import create_engine

def get_database_config_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return data["database"]

def connect_to_db(config_data):
    connection_string = f"mariadb+mariadbconnector://{config_data['user']}:{config_data['password']}@{config_data['host']}:{config_data['port']}/{config_data['name']}"
    engine = create_engine(connection_string)
    return engine.connect()

@hydra.main(config_path="../config", config_name="main", version_base=None)
def main(config: DictConfig):

    config_data = get_database_config_from_json(config.db.credentials)

    print(f"Connecting to database: {config_data['name']}")

    conn = connect_to_db(config_data)

    # Write a SQL query to fetch the 'lang' column from the 'texts' table
    sql_query = "SELECT lang FROM texts"

    df = pd.read_sql_query(sql_query, conn)
    
    output_path = "temp_dataframe.csv"
    df.to_csv(output_path, index=False)
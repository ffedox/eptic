import pandas as pd
import json
from sqlalchemy import create_engine, exc
import hydra
from omegaconf import DictConfig

# Function to read database configuration from JSON file
def get_database_config_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return data["database"]

# Function to connect to the database
def connect_to_db(config_data, db_name=None):
    database_name = db_name if db_name else config_data['name']
    connection_string = f"mariadb+mariadbconnector://{config_data['user']}:{config_data['password']}@{config_data['host']}:{config_data['port']}/{database_name}"
    engine = create_engine(connection_string)
    return engine

# Hydra main function for running the script
@hydra.main(config_path="E:\Code\eptic\config", config_name="main", version_base=None)
def main(config: DictConfig):
    config_data = get_database_config_from_json(config.db.credentials)
    print(f"Connecting to database: {config_data['name']}")

    # Connect to the database using the engine
    engine = connect_to_db(config_data, db_name="noskeptic")

    # Load the Excel file
    excel_file_path = r'E:\Code\eptic\src\noske\final_corpus_noske_renamed_columns_v2.xlsx'
    excel_data = pd.read_excel(excel_file_path)

    # Parse the column names to map them to table and field names
    table_field_mapping = {}
    for column in excel_data.columns:
        table, field = column.split('.')
        if table not in table_field_mapping:
            table_field_mapping[table] = []
        if field not in table_field_mapping[table]:
            table_field_mapping[table].append(field)

    # Bulk insert data for each table
    for table, fields in table_field_mapping.items():
        # Select relevant columns for the current table
        table_data = excel_data[[f"{table}.{field}" for field in fields]]
        table_data.columns = fields  # Renaming columns to match table field names

        # Bulk insert data into the table
        try:
            table_data.to_sql(table, engine, if_exists='append', index=False, chunksize=1000)
            print(f"Data successfully inserted into {table}")
        except Exception as e:
            print(f"An error occurred while inserting data into {table}: {e}")

# Entry point of the script
if __name__ == "__main__":
    main()

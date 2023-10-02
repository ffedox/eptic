import mariadb
import json
from omegaconf import DictConfig
import hydra

def get_database_config_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return data["database"]

@hydra.main(config_path="../config", config_name="main", version_base=None)
def main(config: DictConfig):
    # Use Hydra to get the path to config.json and then get the database config from it
    print(f"Processing data using {config.db.credentials}")

    config_data = get_database_config_from_json(config.db.credentials)

    # Connect to the database using MariaDB connector
    conn = mariadb.connect(
        user=config_data['user'],
        password=config_data['password'],
        host=config_data['host'],
        port=config_data['port'],  
        database=config_data['name']
    )

    cursor = conn.cursor()

    # Execute the query
    cursor.execute("SELECT DISTINCT lang FROM texts")
    
    # Fetch the results
    unique_langs = [row[0] for row in cursor.fetchall()]
    
    for lang in unique_langs:
        print(lang)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
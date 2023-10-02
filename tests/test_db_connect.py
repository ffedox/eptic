import sys
from omegaconf import DictConfig
import hydra
from db_connect import connect_to_db, get_database_config_from_json

def test_connect_to_db():
    config_data = get_database_config_from_json("../config.json")  # Adjust the path as needed
    connection = connect_to_db(config_data)

    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT lang FROM texts")
    unique_langs = [row[0] for row in cursor.fetchall()]
    assert unique_langs, "Unable to fetch unique languages."
    for lang in unique_langs:
        print(lang)

    cursor.close()
    connection.close()

@hydra.main(config_path="../config", config_name="main", version_base=None)
def run_tests(config: DictConfig):
    sys.path.append(config.paths.src)  # Adjusting sys.path using Hydra
    
    # Get the config_data for the database
    config_data = get_database_config_from_json(config.db.credentials)

    # Run the test
    test_connect_to_db()

if __name__ == "__main__":
    run_tests()
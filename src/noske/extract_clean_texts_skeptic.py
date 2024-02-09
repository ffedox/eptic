import os
import sys
import pandas as pd

# Adjusting the sys.path to be able to import the modules from different directories
sys.path.append(r"E:\Code\eptic\src\skeptic")
sys.path.append(r"E:\Code\eptic\src\noske")

# Importing necessary functions
from db_connect import connect_to_db, get_database_config_from_json
import hydra
from omegaconf import DictConfig

@hydra.main(config_path=r"E:\Code\eptic\config", config_name="main", version_base=None)
def main(config: DictConfig):
    # Get database configuration
    config_data = get_database_config_from_json(config.db.credentials)
    
    # Connect to the database
    conn = connect_to_db(config_data)
    
    # Define sql query
    sql_query = """
    SELECT t.*, a.*, e.*, s.*, i.*, u.*
    FROM texts t
    LEFT JOIN alignments a ON t.id = a.id
    LEFT JOIN events e ON t.event_id = e.id
    LEFT JOIN speakers s ON e.speaker_id = s.id
    LEFT JOIN interpreters i ON t.interpreter_id = i.id
    LEFT JOIN users u ON t.user_id = u.id
    """

    # Execute the query and read the result into a DataFrame
    df = pd.read_sql_query(sql_query, conn)

    # Specify the output file path
    output_path = "clean_texts_skeptic.xlsx"

    # Export the DataFrame to an Excel file
    df.to_excel(output_path, index=False)
    
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    main()
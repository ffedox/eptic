import pandas as pd
import hydra
from omegaconf import DictConfig
import sys

# Adjusting the sys.path is necessary only if db_connect and get_database_config_from_json are not in the current directory
sys.path.append(r"E:\Code\eptic\src\skeptic")
sys.path.append(r"E:\Code\eptic\src\noske")

from db_connect import connect_to_db, get_database_config_from_json

@hydra.main(config_path="E:\\Code\\eptic\\config", config_name="main", version_base=None)
def main(config: DictConfig):
    # Get database configuration
    config_data = get_database_config_from_json(config.noskeptic.credentials)
    
    # Connect to the database
    conn = connect_to_db(config_data)
    
    # Define SQL query for the 'texts' table
    sql_query = "SELECT * FROM texts"
    
    # Execute the query and read the result into a DataFrame
    df = pd.read_sql_query(sql_query, conn)
    
    # Specify the output file path
    output_path = "E:\\Code\\eptic\\src\\noske\\texts_dump.xlsx"
    
    # Export the DataFrame to an Excel file
    df.to_excel(output_path, index=False)
    
    print(f"Data from 'texts' table saved to {output_path}")

if __name__ == "__main__":
    main()
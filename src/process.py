import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

from db_connect import connect_to_db, get_database_config_from_json

import hydra
from omegaconf import DictConfig


@hydra.main(config_path="../config", config_name="main", version_base=None)
def process_data(config: DictConfig):
    """Function to process the data"""

    

    print(f"Process data using {config.data.raw}")
    #print(f"Columns used: {config.process.use_columns}")


if __name__ == "__main__":
    process_data()

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

from db_connect import connect_to_db, get_database_config_from_json

import hydra
from omegaconf import DictConfig

@hydra.main(config_path="../config", config_name="main")
def create_graph_langs(cfg: DictConfig):
    # Retrieve database config path using Hydra's cfg object
    config_data = get_database_config_from_json(cfg.db.credentials)

    # Connect to the database
    conn = connect_to_db(config_data)

    # Fetch data from the database
    data = get_lang_counts(conn)
    df = pd.DataFrame(data)

    # Create a color palette
    palette = sns.color_palette("hls", len(data["lang"]))

    # Create a bar chart
    plt.figure(figsize=(10,6))
    ax = sns.barplot(x="lang", y="count", data=df, hue="lang", palette=palette, legend=False)

    # Annotate each bar with its respective count
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 9), 
                    textcoords='offset points')

    plt.title("Samples per Language")
    plt.ylabel("Samples")
    plt.xlabel("Language")

    # Specify the output path using Hydra's cfg object
    output_path = os.path.join(cfg.outputs.graphs, "lang_counts.png")
    plt.savefig(output_path)
    plt.show()

def get_lang_counts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT lang, COUNT(lang) FROM texts GROUP BY lang")
    results = cursor.fetchall()
    cursor.close()
    
    # Convert results into a dictionary
    data = {
        "lang": [row[0] for row in results],
        "count": [row[1] for row in results]
    }
    return data

if __name__ == "__main__":
    create_graph_langs()
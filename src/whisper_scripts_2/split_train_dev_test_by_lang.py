import pandas as pd
import numpy as np
import os

def split_data_and_create_folders(file_path):
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Create directories for train, dev, test
    base_path = os.path.dirname(file_path)
    split_folders = ["train", "dev", "test"]
    for folder in split_folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

    # Group by 'event.id' and 'subset' to ensure they stay together and are balanced
    grouped = df.groupby(['event.id', 'subset'])

    # Lists to hold the indices for each split
    train_indices, dev_indices, test_indices = [], [], []

    # Split the data
    for name, group in grouped:
        # Randomly assign each group to a split
        split = np.random.choice(split_folders, p=[0.7, 0.15, 0.15])
        if split == 'train':
            train_indices.extend(group.index)
        elif split == 'dev':
            dev_indices.extend(group.index)
        else:
            test_indices.extend(group.index)

    # Create DataFrames for each split
    train_df = df.loc[train_indices]
    dev_df = df.loc[dev_indices]
    test_df = df.loc[test_indices]

    # Save the DataFrames in their respective folders
    for split_name, split_df in zip(split_folders, [train_df, dev_df, test_df]):
        split_df.to_excel(os.path.join(base_path, split_name, f'{os.path.basename(file_path)}'), index=False)

    # Print the event.ids in each split
    print("Event IDs in Train:", train_df['event.id'].unique())
    print("Event IDs in Dev:", dev_df['event.id'].unique())
    print("Event IDs in Test:", test_df['event.id'].unique())

    # Print the count of each unique value of 'subset' in each split
    print("\nSubset counts in Train:", train_df['subset'].value_counts().to_dict())
    print("Subset counts in Dev:", dev_df['subset'].value_counts().to_dict())
    print("Subset counts in Test:", test_df['subset'].value_counts().to_dict())

# Example usage
# Replace 'path_to_your_file' with the actual path of the Excel file
split_data_and_create_folders(r'E:\Code\eptic\data\raw\noske_videos\video_audios\english\sentences_noske_english.xlsx')
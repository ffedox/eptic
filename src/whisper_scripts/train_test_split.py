import pandas as pd
import numpy as np

# Load the data with 'event.id' as string to keep leading zeros
file_path = r'E:\Code\eptic\src\noske_per_whisper\sentences_noske_cleaned_with_event_id_5_only_found_audios.xlsx'
df = pd.read_excel(file_path, dtype={'event.id': str})

# Shuffle the unique event.ids
unique_event_ids = df['event.id'].unique()
np.random.shuffle(unique_event_ids)

# Calculate the number of event.ids for the test set (10%)
num_test_ids = int(len(unique_event_ids) * 0.1)

# Split the event.ids into train and test
test_event_ids = unique_event_ids[:num_test_ids]
train_event_ids = unique_event_ids[num_test_ids:]

# Split the data into train and test sets based on event.ids
train_df = df[df['event.id'].isin(train_event_ids)]
test_df = df[df['event.id'].isin(test_event_ids)]

# Save the dataframes into Excel files
train_df.to_excel(r'E:\Code\eptic\src\noske_per_whisper\sentences_noske_cleaned_with_event_id_5_only_found_audios_train.xlsx', index=False)
test_df.to_excel(r'E:\Code\eptic\src\noske_per_whisper\sentences_noske_cleaned_with_event_id_5_only_found_audios_test.xlsx', index=False)

print("Data split into train and test sets and saved to Excel files.")

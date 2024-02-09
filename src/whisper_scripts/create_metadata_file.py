import pandas as pd
import os
import csv

# Load the train and test data
train_file_path = r'E:\Code\eptic\src\noske_per_whisper\sentences_noske_cleaned_with_event_id_5_only_found_audios_train.xlsx'
test_file_path = r'E:\Code\eptic\src\noske_per_whisper\sentences_noske_cleaned_with_event_id_5_only_found_audios_test.xlsx'
train_df = pd.read_excel(train_file_path)
test_df = pd.read_excel(test_file_path)

# Function to process dataframe and add prefix to file names
def process_df(file_path, prefix):
    df = pd.read_excel(file_path)
    df['file_name'] = prefix + "/" + df['audio_file_path'].apply(lambda x: os.path.basename(x))
    # Replace line breaks and commas in the transcription
    df['transcription'] = df['s.text'].str.replace('\n', ' ').replace(',', '')
    return df[['file_name', 'transcription']]

train_processed = process_df(train_file_path, 'train')
test_processed = process_df(test_file_path, 'test')

combined_df = pd.concat([train_processed, test_processed])

# Save to CSV
output_csv_path = r'E:\Code\eptic\src\noske_per_whisper\metadata.csv'
combined_df.to_csv(output_csv_path, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')




import pandas as pd
import re

# Load the Excel file
file_path = r'E:\Code\eptic\src\noske_per_whisper\test_audio_rotti_with_event_id.xlsx'
df = pd.read_excel(file_path)

# Define a function to extract the first 4 digits
def extract_first_4_digits(text):
    match = re.search(r'\d{4}', text)
    return match.group(0) if match else None

# Apply the function to each row in the 'text.id' column and create 'event.id' column
df['event.id'] = df['text.id'].apply(extract_first_4_digits)

# Extracting the 'lang' and 'mode' from 'text.id' column
df['lang'] = df['text.id'].str.extract(r'\d{4}(\w{2})_')[0]
df['mode'] = df['text.id'].str.extract(r'_(\w{2})_')[0]

# Extract the part after the last underscore as 'direction'
df['direction'] = df['text.id'].str.extract(r'.*_(\w+)$')[0]

# Drop rows where mode is not equal to 'sp'
df = df[df['mode'] == 'sp']

# Drop rows where mode is 'sp' but 's.video' is null
df = df.dropna(subset=['s.video'])

# Save the modified DataFrame back to Excel
output_path = r'E:\Code\eptic\src\noske_per_whisper\test_audio_rotti_with_event_id_and_rest.xlsx'
df.to_excel(output_path, index=False)

print("Processing complete. Output saved to:", output_path)

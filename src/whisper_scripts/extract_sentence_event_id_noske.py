import pandas as pd
import re

# Load the Excel file
file_path = r'E:\Code\eptic\src\noske_per_whisper\test_audio_rotti.xlsx'
df = pd.read_excel(file_path)

# Define a function to extract the first 4 digits
def extract_first_4_digits(text):
    match = re.search(r'\d{4}', text)
    return match.group(0) if match else None

# Apply the function to each row in the 'text.id' column and create 'event.id' column
df['event.id'] = df['text.id'].apply(extract_first_4_digits)

# Save the modified DataFrame back to Excel
output_path = r'E:\Code\eptic\src\noske_per_whisper\test_audio_rotti_with_event_id.xlsx'
df.to_excel(output_path, index=False)

print("Processing complete. Output saved to:", output_path)

import pandas as pd

# Load the Excel file
file_path = r'E:\Code\eptic\src\noske_per_whisper_2\sentences_noske_cleaned_with_event_id.xlsx'
df = pd.read_excel(file_path)

# Extract the last two characters from 'text.id' and create a new column 'direction'
#df['direction'] = df['text.id'].str[-2:]

def determine_subset(row):
    if row['mode'] == 'sp' and row['direction'] == 'tt':
        return 'interpreted'
    elif row['mode'] == 'sp' and row['direction'] == 'st':
        return 'l2' if row['speaker.native'] == 'n' else 'l1'
    else:
        return None  # or some default value if necessary

df['subset'] = df.apply(determine_subset, axis=1)

# Optionally, save the modified DataFrame back to an Excel file
df.to_excel(r'E:\Code\eptic\src\noske_per_whisper_2\sentences_noske_cleaned_with_event_id.xlsx', index=False)
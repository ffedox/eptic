import pandas as pd
import re

# Load the file
file_path = r'E:\Code\eptic\src\noske\final_corpus_noske_renamed_columns.xlsx'
df = pd.read_excel(file_path)

# Function to extract the prefix
def extract_prefix(text_id):
    text_id_str = str(text_id)
    if re.match(r'^\d+', text_id_str) and not text_id_str.isdigit():
        return re.match(r'^\d+', text_id_str).group()
    return None

# Create the mapping
df['prefix'] = df['texts.id'].apply(extract_prefix)
unique_prefixes = df['prefix'].dropna().unique()
mapping = {prefix: str(i + 223) for i, prefix in enumerate(unique_prefixes)}

# Apply the mapping to 'texts.event_id' only for rows where 'texts.event_id' is empty
df['texts.event_id'] = df.apply(lambda row: mapping.get(extract_prefix(row['texts.id']), row['texts.id']) 
                                if pd.isna(row['texts.event_id']) or row['texts.event_id'] == '' 
                                else row['texts.event_id'], axis=1)

# Remove the temporary column
del df['prefix']

# Save the updated file
output_excel_path = r'E:\Code\eptic\src\noske\final_corpus_noske_with_ids.xlsx'
df.to_excel(output_excel_path, index=False)
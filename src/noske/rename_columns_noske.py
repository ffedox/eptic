import pandas as pd
import re

# Paths for the input files
file_corpus = r'E:\Code\eptic\src\noske\final_corpus_noske_not_present.xlsx'
file_correspondences = r'E:\Code\eptic\docs\modified_correspondences.xlsx'
noske_present_path = r'E:\Code\eptic\src\noske\final_corpus_noske_present.xlsx'
duplicate_texts_path = r'E:\Code\eptic\src\noske\duplicate_texts.xlsx'
output_path_modified = r'E:\Code\eptic\src\noske\final_corpus_noske_renamed_columns.xlsx'

# Read the Excel files into Pandas DataFrames
df_corpus = pd.read_excel(file_corpus)
df_correspondences = pd.read_excel(file_correspondences)
noske_present_df = pd.read_excel(noske_present_path)
df_duplicate_texts = pd.read_excel(duplicate_texts_path)

# Renaming and adding columns based on 'modified_correspondences.xlsx'
for index, row in df_correspondences.iterrows():
    skeptic_column = row['skeptic'].strip()  # Trim any whitespace
    noske_column = row['noske']

    if pd.notna(noske_column):
        noske_column = noske_column.strip()
        if noske_column in df_corpus.columns:
            df_corpus.rename(columns={noske_column: skeptic_column}, inplace=True)
    else:
        if skeptic_column not in df_corpus.columns:
            df_corpus[skeptic_column] = ''

# Additional operations for filtering and reordering columns...
renamed_or_added_columns = set(df_correspondences['skeptic'].dropna().str.strip())
noske_columns = set(df_correspondences['noske'].dropna().str.strip())
columns_to_keep = renamed_or_added_columns.union(noske_columns)
filtered_df_corpus = df_corpus.loc[:, df_corpus.columns.intersection(columns_to_keep)]
missing_columns = set(df_correspondences['skeptic'].dropna().str.strip()) - set(filtered_df_corpus.columns)
for column in missing_columns:
    filtered_df_corpus[column] = ''
column_order_prefixes = ["texts.", "alignments.", "events.", "speakers.", "interpreters.", "users."]
ordered_columns = []
for prefix in column_order_prefixes:
    ordered_columns.extend([col for col in filtered_df_corpus.columns if col.startswith(prefix)])
remaining_columns = [col for col in filtered_df_corpus.columns if col not in ordered_columns]
ordered_columns.extend(remaining_columns)
ordered_df_corpus = filtered_df_corpus[ordered_columns]

# Function to extract only the language code from the text_id
def extract_lang(text_id):
    match = re.search(r'^\d{4}([a-z]+)_', str(text_id).lower())
    return match.group(1) if match else None

# Apply the function to fill the 'texts.lang' column
ordered_df_corpus['texts.lang'] = ordered_df_corpus['texts.id'].apply(extract_lang)

# Function to compare and find matches for event IDs
def compare_and_find_event_id(text_id):
    if pd.isna(text_id):
        return None  # Return None for NaN values

    first_four_chars = str(text_id)[:4]  # Extract the first four characters
    # Filter df_duplicate_texts for rows where 'id' starts with first_four_chars
    matching_rows = df_duplicate_texts[df_duplicate_texts['id'].str.startswith(first_four_chars, na=False)]
    if not matching_rows.empty:
        # Get the 'matching_event_id' from the first matching row
        return matching_rows.iloc[0]['matching_event_id']
    else:
        return None

# Apply the function to the 'texts.id' column and update 'texts.event_id'
ordered_df_corpus['texts.event_id'] = ordered_df_corpus['texts.id'].apply(compare_and_find_event_id)

# Save the modified DataFrame to an Excel file
ordered_df_corpus.to_excel(output_path_modified, index=False)
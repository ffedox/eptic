import pandas as pd

# Define the path to the Excel files
duplicate_texts_file_path = 'E:\\Code\\eptic\\src\\noske\\duplicate_texts.xlsx'
skeptic_file_path = 'E:\\Code\\eptic\\src\\noske\\clean_texts_skeptic.xlsx'
noske_file_path = 'E:\\Code\\eptic\\src\\noske\\clean_texts_noske.xlsx'

# Load the 'duplicate_texts.xlsx' Excel file
df = pd.read_excel(duplicate_texts_file_path)

# Convert values to strings and save unique values from 'id' and 'matching_text_id' into a set
unique_values = set(df['id'].astype(str)).union(set(df['matching_text_id'].astype(str)))

# Separate the unique values into two lists
numbers_only = [value for value in unique_values if value.isdigit()]
includes_characters = [value for value in unique_values if not value.isdigit()]

# Load the 'skeptic_texts_clean.xlsx' file
skeptic_df = pd.read_excel(skeptic_file_path)

# Convert 'id' in skeptic_df to string to ensure proper comparison
skeptic_df['id'] = skeptic_df['id'].astype(str)

# Filter rows where 'id' is present in the numbers_only list
already_present_df = skeptic_df[skeptic_df['id'].isin(numbers_only)]

# Filter rows where 'id' is not present in the numbers_only list
not_present_df = skeptic_df[~skeptic_df['id'].isin(numbers_only)]

# Load the 'noske_texts_clean.xlsx' file
noske_df = pd.read_excel(noske_file_path)

# Convert 'text.id' in noske_df to string to ensure proper comparison
noske_df['text.id'] = noske_df['text.id'].astype(str)

# Filter rows where 'text.id' is not present in the includes_characters list
final_corpus_not_present_df = noske_df[~noske_df['text.id'].isin(includes_characters)]

# Filter rows where 'text.id' is present in the includes_characters list
final_corpus_present_df = noske_df[noske_df['text.id'].isin(includes_characters)]

# Define paths for the output files
#output_path_present = 'E:\\Code\\eptic\\src\\noske\\final_corpus_skeptic_already_present.xlsx'
#output_path_not_present = 'E:\\Code\\eptic\\src\\noske\\final_corpus_skeptic_not_present.xlsx'
output_path_noske_not_present = 'E:\\Code\\eptic\\src\\noske\\final_corpus_noske_not_present.xlsx'
output_path_noske_present = 'E:\\Code\\eptic\\src\\noske\\final_corpus_noske_present.xlsx'

# Save the filtered dataframes to Excel files
# already_present_df.to_excel(output_path_present, index=False)
# not_present_df.to_excel(output_path_not_present, index=False)
final_corpus_not_present_df.to_excel(output_path_noske_not_present, index=False)
final_corpus_present_df.to_excel(output_path_noske_present, index=False)
import pandas as pd

# Define the paths to your Excel files
path_to_output_1 = r"E:\Code\eptic\src\noske\levenshtein_distance_skeptic.xlsx"
path_to_output_2 = r"E:\Code\eptic\src\noske\levenshtein_distance_noske.xlsx"

# Load the Excel files
df_output_1 = pd.read_excel(path_to_output_1)
df_output_2 = pd.read_excel(path_to_output_2)

# Select the desired columns from df_output_1, including the 'lang' column
df_filtered_1 = df_output_1[df_output_1['levenshtein_distance'] < 10][
    ['id', 'original_text', 'levenshtein_distance', 'matching_text_id', 'matching_cleaned_text', 'lang']
]
# Rename 'matching_cleaned_text' to 'matching_original_text' for consistency
df_filtered_1.rename(columns={'matching_cleaned_text': 'matching_original_text'}, inplace=True)

# Select the desired columns from df_output_2 and extract the 'lang' from the 'text.id' column
df_filtered_2 = df_output_2[df_output_2['levenshtein_distance'] < 10][
    ['text.id', 'original_text', 'levenshtein_distance', 'matching_text_id', 'matching_text', 'matching_event_id']
]
# Extract 'lang' from 'text.id' and add it to the dataframe
df_filtered_2['lang'] = df_filtered_2['text.id'].str.extract(r'^\d{4}([a-z]{2})', expand=False)
# Rename 'text.id' column in df_filtered_2 to 'id' and 'matching_text' to 'matching_original_text' for consistency
df_filtered_2.rename(columns={'text.id': 'id', 'matching_text': 'matching_original_text'}, inplace=True)

# Combine the filtered data
df_combined = pd.concat([df_filtered_1, df_filtered_2], axis=0, ignore_index=True)

# Sort based on Levenshtein distance
df_combined_sorted = df_combined.sort_values(by='levenshtein_distance', ascending=True)

# Remove all rows where lang='sl'
df_combined_filtered = df_combined_sorted[df_combined_sorted['lang'] != 'sl']

# Save the combined DataFrame to a new Excel file
output_path = r"E:\Code\eptic\src\noske\duplicate_texts.xlsx"
df_combined_filtered.to_excel(output_path, index=False)

print(f"Duplicate texts saved to {output_path}")
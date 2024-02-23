import pandas as pd

# Paths to the Excel files
file_1_path = r'E:\Code\eptic\docs\clean_texts_skeptic_new_for_final_merging.xlsx'
file_2_path = 'E:\\Code\\eptic\\src\\noske\\final_corpus_noske_with_ids.xlsx'

# Load the Excel files into pandas DataFrames
df1 = pd.read_excel(file_1_path)
df2 = pd.read_excel(file_2_path)

# Merge the DataFrames on top of each other
merged_df = pd.concat([df1, df2], ignore_index=True)

# Save the merged DataFrame to a new Excel file
output_path = 'E:\\Code\\eptic\\src\\noske\\final_corpus_noskeptic2.xlsx'
merged_df.to_excel(output_path, index=False)

print(f"Merged file saved to {output_path}")

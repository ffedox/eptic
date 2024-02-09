import pandas as pd
import os
import re

directory_path = r'E:\Code\eptic\data\raw\noske\EPTIC11_v2'

# Function to extract data from a .vert file with updated text cleaning logic
def extract_data_from_vert(file_path):
    data = []
    current_attributes = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        inside_s_tag = False
        s_text = []
        
        for line in lines:
            stripped_line = line.strip()
            
            # Extract attributes from <text>, <speaker>, <st>, and <interpreter> tags
            if stripped_line.startswith(('<text', '<speaker', '<st', '<interpreter')):
                tag = stripped_line.split(' ')[0][1:]  # Extract the tag name
                current_attributes.update({f'{tag}.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)})
            
            # Process <s> tag
            elif stripped_line.startswith('<s'):
                inside_s_tag = True
                s_text = []
                s_attributes = {f's.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                current_attributes.update(s_attributes)

            elif stripped_line.startswith('</s>'):
                inside_s_tag = False
                formatted_s_text = ''
                for text in s_text:
                    if text.startswith('<g/>'):
                        # Remove space before <g/> if there is one
                        formatted_s_text = formatted_s_text.rstrip()
                    else:
                        formatted_s_text += text.split('\t')[0] + ' '
                formatted_s_text = formatted_s_text.strip()
                row = {**current_attributes, **s_attributes, 's.text': formatted_s_text}
                data.append(row)

            # Process text within <s> tag
            elif inside_s_tag:
                s_text.append(stripped_line)

    return pd.DataFrame(data)

# Process all .vert files in the directory and store results
all_dfs = []
for filename in os.listdir(directory_path):
    if filename.endswith(".vert"):
        file_path = os.path.join(directory_path, filename)
        df = extract_data_from_vert(file_path)
        all_dfs.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(all_dfs, ignore_index=True)

# Save the cleaned and combined DataFrame to an Excel file
output_filepath_cleaned = r'E:\Code\eptic\src\noske_per_whisper\sentences_noske_cleaned.xlsx'
combined_df.to_excel(output_filepath_cleaned, index=False, engine='openpyxl')

output_filepath_cleaned
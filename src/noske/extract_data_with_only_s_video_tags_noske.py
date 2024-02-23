import os
import re
import pandas as pd

# Directory path
directory_path = r"E:\Code\eptic\data\raw\noske\EPTIC11_v2"

# List to store the dataframes from each file
dfs = []


# Redefined function to process .vert files according to the new requirement
def extract_data_from_vert_v3(file_path):
    data = []
    current_text_attributes = {}
    current_speaker_attributes = {}
    current_st_attributes = {}
    current_interpreter_attributes = {}
    s_content = ''
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            
            if stripped_line.startswith('<text'):
                current_text_attributes = {f'text.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                
            elif stripped_line.startswith('<speaker'):
                current_speaker_attributes = {f'speaker.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                
            elif stripped_line.startswith('<st'):
                current_st_attributes = {f'st.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                
            elif stripped_line.startswith('<interpreter'):
                current_interpreter_attributes = {f'interpreter.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                
            elif stripped_line.startswith('<s'):
                # Extract attributes for <s> tag
                s_attributes = {f's.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                s_content = ''
                
            elif stripped_line.startswith('</s>'):
                # Append the current sentence content to the data list
                data.append({**current_text_attributes, **current_speaker_attributes, **current_st_attributes, **current_interpreter_attributes, **s_attributes, 's.content': s_content})
                
            elif not stripped_line.startswith('<'):
                # Extract only the first word from each line within <s> tags
                first_word = stripped_line.split()[0] if stripped_line.split() else ''
                s_content += first_word + " "
                
    return data

for filename in os.listdir(directory_path):
    if filename.endswith(".vert"):
        file_path = os.path.join(directory_path, filename)
        
        extracted_data = extract_data_from_vert_v3(file_path)
        
        dfs.append(pd.DataFrame(extracted_data))

# Concatenate all the dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Ensure that there are no "NA" values
combined_df = combined_df.where(pd.notna(combined_df), None)

# Save the combined dataframe to an Excel file
output_excel_path = os.path.join(directory_path, "noske_texts_with_tags.xlsx")
combined_df.to_excel(output_excel_path, index=False)

print(f"Processed data saved to: {output_excel_path}")
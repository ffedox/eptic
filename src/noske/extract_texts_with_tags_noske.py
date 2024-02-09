import os
import re
import pandas as pd

# Directory path
directory_path = r"E:\Code\eptic\data\raw\noske\EPTIC11_v2"

# List to store the dataframes from each file
dfs = []

# Redefining the function to extract data based on the updated requirements
def extract_data_from_vert_v3(file_path):
    # Data to be collected
    data = []
    
    # Flags and placeholders for attributes and content
    current_text_attributes = {}
    current_speaker_attributes = {}
    current_st_attributes = {}
    current_interpreter_attributes = {}
    concatenated_s_content = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
        for line in lines:
            stripped_line = line.strip()
            
            # Extract attributes for <text> tag
            if stripped_line.startswith('<text'):
                current_text_attributes = {f'text.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                
            # Extract attributes for <speaker> tag
            elif stripped_line.startswith('<speaker'):
                current_speaker_attributes = {f'speaker.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                
            # Extract attributes for <st> tag
            elif stripped_line.startswith('<st'):
                current_st_attributes = {f'st.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                
            # Extract attributes for <interpreter> tag
            elif stripped_line.startswith('<interpreter'):
                current_interpreter_attributes = {f'interpreter.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                
            # Handling <s> tags
            elif stripped_line.startswith('<s'):
                s_attributes = {f's.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                s_text = stripped_line + " "
            elif stripped_line.startswith('</s>'):
                formatted_s_text = s_text + ' '.join([x.split('\t')[0] for x in stripped_line.splitlines() if not x.startswith('<g/>')])
                concatenated_s_content.append(formatted_s_text)
            elif stripped_line.startswith('</text>'):
                merged_s_text = ' '.join(concatenated_s_content)
                merged_attributes = {**current_text_attributes, **current_speaker_attributes, **current_st_attributes, **current_interpreter_attributes, 's.text': merged_s_text}
                data.append(merged_attributes)
                concatenated_s_content = []  # Reset for the next <text> block
            else:
                s_text += stripped_line + " "
                
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

import pandas as pd
import re
import os

# Function to extract data from a .vert file
def extract_data_from_vert(file_path):
    data = []
    current_text_attributes = {}
    current_speaker_attributes = {}
    current_st_attributes = {}
    current_interpreter_attributes = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        inside_s_tag = False
        s_text = []
        
        for line in lines:
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
                inside_s_tag = True
                s_attributes = {f's.{m.group(1)}': m.group(2) for m in re.finditer(r'(\w+)="([^"]+)"', stripped_line)}
                s_text = []
            elif stripped_line.startswith('</s>'):
                inside_s_tag = False
                formatted_s_text = ''
                for i in range(len(s_text)):
                    if s_text[i].startswith('<g/>'):
                        if i > 0:
                            formatted_s_text = formatted_s_text.rstrip()
                        continue
                    formatted_s_text += s_text[i].split('\t')[0] + ' '
                formatted_s_text = formatted_s_text.strip()
                s_attributes['s.text'] = formatted_s_text
                merged_attributes = {**current_text_attributes, **current_speaker_attributes, **current_st_attributes, **current_interpreter_attributes, **s_attributes}
                data.append(merged_attributes)
            elif inside_s_tag:
                s_text.append(stripped_line)
                
    df = pd.DataFrame(data)
    df = df.where(pd.notna(df), None)
    return df

# Function to process a DataFrame
def process_dataframe(df):
    # 1. Merge s.text values based on unique text.id
    df['s.text_processed'] = df.groupby('text.id')['s.text'].transform(lambda x: ' '.join(x))
    
    # 2. Ensure each text.id appears only once in the output
    df_unique = df.drop_duplicates(subset='text.id')
    
    # 3. Drop the columns s.id, s.video, and s.text
    df_unique = df_unique.drop(columns=['s.id', 's.video', 's.text'], errors='ignore')
    
    # 4. Remove the interpreter.id column if it exists
    # if 'interpreter.id' in df_unique.columns:
        # df_unique = df_unique.drop(columns='interpreter.id')
        
    # 5. Ensure that the order of text.id stays the same after the merging
    df_unique = df_unique.sort_values(by='text.id')
    
    # 6. Extract last 5 characters from text.id
    df_unique['last_5_chars'] = df_unique['text.id'].str[-5:]
    
    # 7. Extract the part before and after "_" from the last 5 characters
    df_unique[['spoken_written', 'source_target']] = df_unique['last_5_chars'].str.split('_', expand=True)
    
    # 8. Handle special case when text.id ends with "tt_in_sl"
    mask = df_unique['text.id'].str.endswith('tt_in_sl')
    df_unique.loc[mask, 'spoken_written'] = 'sp'
    df_unique.loc[mask, 'source_target'] = 'tt'
    
    # 9. Capitalize spoken_written and source_target columns
    df_unique['spoken_written'] = df_unique['spoken_written'].str.upper()
    df_unique['source_target'] = df_unique['source_target'].str.upper()
    
    # 10. Drop the temporary column
    df_unique = df_unique.drop(columns='last_5_chars')
    
    return df_unique

def main():
    dfs = []
    vert_files_directory = 'E:\\Code\\eptic\\data\\raw\\noske\\EPTIC11_v2'

    # Loop over all .vert files in the specified directory
    for filename in os.listdir(vert_files_directory):
        if filename.endswith(".vert"):
            file_path = os.path.join(vert_files_directory, filename)
            
            # Extract data from the .vert file
            df = extract_data_from_vert(file_path)
            
            # Process the DataFrame
            df_processed = process_dataframe(df)
            
            # Add the processed DataFrame to the list
            dfs.append(df_processed)

    if dfs:
        # Concatenate all DataFrames in the list
        df_combined = pd.concat(dfs, ignore_index=True)

        # Save the combined processed data to an Excel file in the current working directory
        output_filepath = "clean_texts_noske.xlsx"
        df_combined.to_excel(output_filepath, index=False, engine='openpyxl')
        print(f"Processed data saved to {output_filepath}")
    else:
        print(f"No .vert files found in the directory {vert_files_directory}.")

if __name__ == "__main__":
    main()
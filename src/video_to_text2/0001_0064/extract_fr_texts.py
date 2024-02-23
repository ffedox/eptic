# Correctly re-import necessary libraries and re-define functions
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
import re

# Load the Excel file again
df_fr = pd.read_excel("D:\\video\\src\\video_to_text\\0001_0064\\file_to_get_txt4.xlsx")

# Preprocessing function for French texts
def preprocess_text_fr(text):
    # Replace '. ' with '.\n' to separate sentences with a newline
    text = re.sub(r'\. ', '.\n', text)
    return text.strip()

# Update filename generation function for French
def generate_filename_fr(noske_id):
    # Extract the first 4 digits from noske_id and append '_fr'
    if pd.notnull(noske_id) and len(noske_id) >= 4:
        return noske_id[:4] + "_fr.txt"
    else:
        return "unknown_fr.txt"

# Apply preprocessing
df_fr['processed_text'] = df_fr['texts.plain_text'].apply(preprocess_text_fr)

# Initialize zip buffer for French texts
zip_buffer_fr = BytesIO()
with ZipFile(zip_buffer_fr, 'w') as zip_file:
    for _, row in df_fr.iterrows():
        file_name = generate_filename_fr(row['texts.noske_id'])
        zip_file.writestr(file_name, row['processed_text'])
zip_buffer_fr.seek(0)

# Define the path for the French zip file
zip_file_path_fr = "D:\\video\\src\\video_to_text\\0001_0064\\fr\\texts_fr_new.zip"

# Save the zip file
with open(zip_file_path_fr, 'wb') as f_out:
    f_out.write(zip_buffer_fr.getvalue())

zip_file_path_fr
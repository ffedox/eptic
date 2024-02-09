import os
import pandas as pd

# Load the Excel file
file_path = r'E:\Code\eptic\src\noske_per_whisper_2\sentences_noske_cleaned_with_event_id.xlsx'
df = pd.read_excel(file_path)

# Create directories
base_path = r'E:\Code\eptic\data\raw\noske_videos\video_audios'
directories = ["english", "french", "italian", "slovenian"]
for dir_name in directories:
    os.makedirs(os.path.join(base_path, dir_name), exist_ok=True)

# Filter and save the DataFrame based on language
languages = {'en': 'english', 'fr': 'french', 'it': 'italian', 'sl': 'slovenian'}
for lang_code, folder_name in languages.items():
    filtered_df = df[df['lang'] == lang_code]
    save_path = os.path.join(base_path, folder_name, f'sentences_noske_{folder_name}.xlsx')
    filtered_df.to_excel(save_path, index=False)

# Verify the creation of the directories
created_directories = os.listdir(base_path)
created_directories, os.listdir(os.path.join(base_path, 'english')) # Displaying contents of one directory as a sample

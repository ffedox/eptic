import pandas as pd
import os

# Path to the directory containing audio files
audio_dir = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios'

# Path to the Excel file
excel_file = 'E:\\Code\\eptic\\src\\noske_per_whisper\\sentences_noske_cleaned_with_event_id_5.xlsx'

# Read the Excel file
df = pd.read_excel(excel_file, dtype={'event.id': str, 's.id': str})

# List all files in the audio directory
audio_files = os.listdir(audio_dir)

# New column for audio file paths
df['audio_file_path'] = ''

# Construct the expected filename for each row and check for its existence
for index, row in df.iterrows():
    s_id_parts = row['s.id'].split(':')
    s_id = s_id_parts[1] if len(s_id_parts) > 1 else s_id_parts[0]  # Use the part after the colon if it exists
    expected_filename = f'audio_{row["event.id"]}_{s_id}_{row["lang"]}_{row["mode"]}_{row["direction"]}.mp3'
    
    for audio_file in audio_files:
        if audio_file == expected_filename:
            df.at[index, 'audio_file_path'] = os.path.join(audio_dir, audio_file)
            break

# Save the updated DataFrame back to the Excel file
df.to_excel(excel_file, index=False)

print("Updated Excel file with audio file paths.")

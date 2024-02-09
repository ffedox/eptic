import pandas as pd
import os
import subprocess
import json

def check_single_audio_track(folder_path):
    single_audio_track_files = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
            file_path = os.path.join(folder_path, filename)
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'a',
                '-show_entries', 'stream=index',
                '-of', 'json',
                file_path
            ]

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            try:
                output = json.loads(result.stdout)
                audio_streams = output.get('streams', [])
                if len(audio_streams) == 1:
                    single_audio_track_files.append(filename)
            except json.JSONDecodeError:
                print(f"Error processing {filename}: Unable to decode ffprobe output")

    return single_audio_track_files

# Paths
video_folder = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\videos_all_languages'
excel_file_path = r'E:\Code\eptic\src\noske\final_corpus_noskeptic.xlsx'

# Read Excel file
df = pd.read_excel(excel_file_path)

# Get videos with single audio track
single_audio_track_files = check_single_audio_track(video_folder)

# Update DataFrame
for filename in os.listdir(video_folder):
    if filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv')) and filename not in single_audio_track_files:
        video_id = filename.split('.')[0]  # Extract ID from filename
        # Find matching rows and update, overwriting existing values in 'texts.video_url'
        mask = df['texts.noske_id'].str.startswith(video_id, na=False) & \
               ~df['texts.noske_id'].str.endswith(('_wr_st', '_wr_tt'), na=False)
        if any(mask):
            df.loc[mask, 'texts.video_url'] = os.path.join(video_folder, filename)

# Save updated DataFrame
df.to_excel(r'E:\Code\eptic\src\noske\final_corpus_noskeptic.xlsx', index=False)



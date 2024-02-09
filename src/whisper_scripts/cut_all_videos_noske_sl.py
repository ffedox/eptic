import pandas as pd
import subprocess
import os
import re

def extract_audio_stream(file_path, language_code, start_time, end_time, output_file):
    # Adjust language code for .wmv files
    if file_path.endswith('.wmv'):
        language_code_map = {'en': 'eng', 'fr': 'fre', 'it': 'ita', 'sl': 'slv'}
    else:  # For .mp4 and other formats
        language_code_map = {'en': 'eng', 'fr': 'fra', 'it': 'ita', 'sl': 'slv'}

    # Use the correct language code based on the file format
    adjusted_language_code = language_code_map.get(language_code, language_code)

    # Construct the ffmpeg command
    command = [
        'ffmpeg',
        '-i', file_path,
        '-map', f'0:m:language:{adjusted_language_code}',
        '-ss', start_time,
        '-to', end_time,
        '-c:a', 'libmp3lame',
        '-q:a', '2',
        output_file
    ]

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"Error in extracting audio: {result.stderr.decode()}")
    else:
        print(f"Audio extracted to {output_file}")

# File paths
excel_file_path = r'E:\Code\eptic\src\noske_per_whisper\test_audio_rotti_with_event_id_and_rest.xlsx'
output_dir = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios\\video_audios_tests'
video_dir = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\videos_all_languages'

# Read the Excel file
df = pd.read_excel(excel_file_path, dtype={'event.id': str, 's.id': str})

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

for index, row in df.iterrows():
    event_id = row['event.id']
    lang = row['lang']
    s_id_parts = row['s.id'].split(':')
    s_id = s_id_parts[1] if len(s_id_parts) > 1 else s_id_parts[0]  # Use the part after the colon if it exists
    mode = row['mode']
    direction = row['direction']

    # Extract start and end times from the video URL
    times = re.search(r'start=(.*?)&end=(.*)', row['s.video'])
    if not times:
        print(f"Invalid time format for row {index}")
        continue
    start_time, end_time = times.groups()

    # Find the corresponding video file
    video_file_mp4 = os.path.join(video_dir, f'{event_id}.mp4')
    video_file_wmv = os.path.join(video_dir, f'{event_id}.wmv')
    video_file = video_file_mp4 if os.path.exists(video_file_mp4) else video_file_wmv

    if not os.path.exists(video_file):
        print(f"File for event ID {event_id} not found.")
        continue

    # Define the output file name using event.id, s.id, language code, mode, and direction
    output_file = os.path.join(output_dir, f'audio_{event_id}_{s_id}_{lang}_{mode}_{direction}.mp3')

    print(f"Processing row {index}: video_file={video_file}, start_time={start_time}, end_time={end_time}, output_file={output_file}")

    # Extract the audio stream
    extract_audio_stream(video_file, lang, start_time, end_time, output_file)

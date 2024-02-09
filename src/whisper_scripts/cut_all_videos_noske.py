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

    # Construct the ffmpeg command to extract and re-encode the specific audio stream
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

    print("Running FFmpeg command:", ' '.join(command))

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("Command result:", result)

    if result.returncode != 0:
        print(f"Error in extracting audio: {result.stderr.decode()}")
    else:
        print(f"Audio extracted to {output_file}")

# Read the Excel file with specific dtype for event.id and s.id
file_path = 'E:\\Code\\eptic\\src\\noske_per_whisper\\sentences_noske_cleaned_with_event_id_5.xlsx'
df = pd.read_excel(file_path, dtype={'event.id': str, 's.id': str})

# Create the output directory if it doesn't exist
output_dir = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios'
os.makedirs(output_dir, exist_ok=True)

# Language code mapping
lang_map = {'en': 'eng', 'fr': 'fra', 'it': 'ita', 'sl': 'slv'}

for index, row in df.iterrows():
    video_url = row['s.video']
    event_id = row['event.id']
    lang = row['lang']
    s_id = row['s.id']
    mode = row['mode']  # Assuming 'mode' column exists in the DataFrame
    direction = row['direction']  # Get the 'direction' column value

    # Extract start and end times from the video URL
    times = re.search(r'start=(.*?)&end=(.*)', video_url)
    if not times:
        continue
    start_time, end_time = times.groups()

    # Find the corresponding video file
    video_file = f'E:\\Code\\eptic\\data\\raw\\noske_videos\\videos_all_languages\\{event_id}.mp4'
    if not os.path.exists(video_file):
        video_file = video_file.replace('.mp4', '.wmv')
        if not os.path.exists(video_file):
            print(f"File for event ID {event_id} not found.")
            continue

    # Define the output file name using event.id, s.id, language code, mode, and direction
    output_file = os.path.join(output_dir, f'audio_{event_id}_{s_id}_{lang}_{mode}_{direction}.mp3')

    print(f"Processing row {index}: video_file={video_file}, start_time={start_time}, end_time={end_time}, output_file={output_file}")

    # Extract the audio stream
    extract_audio_stream(video_file, lang_map.get(lang, 'eng'), start_time, end_time, output_file)

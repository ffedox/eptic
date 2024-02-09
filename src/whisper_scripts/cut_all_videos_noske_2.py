import pandas as pd
import subprocess
import os
import re

def extract_audio_stream(file_path, language_code, start_time, end_time, output_file):
    # Construct the ffmpeg command to extract, trim, and re-encode the specific audio stream
    command = [
        'ffmpeg', 
        '-i', file_path,                                # Input file
        '-map', f'0:m:language:{language_code}',        # Select the specific audio stream by language
        '-ss', start_time,                              # Start time for trimming
        '-to', end_time,                                # End time for trimming
        '-c:a', 'libmp3lame',                           # Re-encode audio to MP3
        '-q:a', '2',                                    # Set audio quality. Range is 0-9; lower means better quality
        output_file                                     # Output file
    ]

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"Error in extracting audio: {result.stderr.decode()}")
    else:
        print(f"Audio extracted to {output_file}")

# Read the Excel file
file_path = 'E:\\Code\\eptic\\src\\noske_per_whisper\\sentences_noske_cleaned_with_event_id_2.xlsx'
df = pd.read_excel(file_path)

# Create the output directory if it doesn't exist
output_dir = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios'
os.makedirs(output_dir, exist_ok=True)

for index, row in df.iterrows():
    video_url = row['s.video']
    event_id = row['event.id']
    lang = row['lang']

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
            continue

    # Define the output file name
    output_file = os.path.join(output_dir, f'audio_{event_id}_{index}.mp3')

    print(f"Processing row {index}: video_file={video_file}, start_time={start_time}, end_time={end_time}, output_file={output_file}")

    # Extract and trim the audio stream
    extract_audio_stream(video_file, lang, start_time, end_time, output_file)

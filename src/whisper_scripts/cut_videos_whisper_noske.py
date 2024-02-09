import subprocess
import os

def extract_audio_stream(file_path, language_code, output_file):
    # Construct the ffmpeg command to extract and re-encode the specific audio stream
    command = [
        'ffmpeg', 
        '-i', file_path,              # Input file
        '-map', f'0:m:language:{language_code}', # Select the specific audio stream by language
        '-c:a', 'libmp3lame',         # Re-encode audio to MP3
        '-q:a', '2',                  # Set audio quality. Range is 0-9; lower means better quality
        output_file                   # Output file
    ]

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"Error in extracting audio: {result.stderr.decode()}")
    else:
        print(f"Audio extracted to {output_file}")

# Replace with your video file path
file_path = r'E:\Code\eptic\data\raw\noske_videos\videos_all_languages\0003.wmv'

# Define the language code you want to extract
language_code = 'eng'

# Define the output file name
output_file = os.path.join(os.path.dirname(__file__), 'extracted_audio.mp3')

extract_audio_stream(file_path, language_code, output_file)

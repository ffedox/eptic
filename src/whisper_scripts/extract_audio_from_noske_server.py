import requests
import subprocess
import os

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def extract_audio(video_file, start_time, end_time, output_file):
    command = [
        'ffmpeg',
        '-i', video_file,
        '-ss', start_time,
        '-to', end_time,
        '-c:a', 'libmp3lame',
        '-q:a', '2',
        output_file
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# URL of the video file
video_url = 'http://amelia.sslmit.unibo.it/video/0032it_sp_tt.mp4'
# Local path to save the video file
video_file_path = '0001it_sp_tt.mp4'
# Start and end times for the audio clip
start_time = '00:13.0'
end_time = '01:27.0'
# Output file name for the MP3
output_mp3 = 'extracted_audio_it.mp3'

# Download the video file
print("Downloading video...")
download_file(video_url, video_file_path)

# Extract the audio segment
print("Extracting audio...")
extract_audio(video_file_path, start_time, end_time, output_mp3)

print(f"Audio extracted to {output_mp3}")

# Optional: Remove the downloaded video file if it's no longer needed
os.remove(video_file_path)
print(f"Removed the video file: {video_file_path}")

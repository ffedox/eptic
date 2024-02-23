import subprocess
import glob
import os

# Directory containing the video files
video_dir = 'D:\\video\\src\\video_to_text\\0001_0064'
# Subdirectory to save the extracted MP3 files
output_dir = os.path.join(video_dir, 'fr')

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# The index of the French audio track
audio_track_index = '1'

# Find all .wmv files in the directory
wmv_files = glob.glob(os.path.join(video_dir, '*.wmv'))

for video_path in wmv_files:
    # Construct the output MP3 file path
    base_filename = os.path.basename(video_path)
    mp3_filename = base_filename.replace('.wmv', '_fr.mp3')
    mp3_path = os.path.join(output_dir, mp3_filename)

    # Construct the ffmpeg command
    command = [
        'ffmpeg',
        '-i', video_path,
        '-map', f'0:{audio_track_index}',
        '-c:a', 'libmp3lame',
        '-q:a', '4',
        mp3_path
    ]

    # Execute the command
    subprocess.run(command)
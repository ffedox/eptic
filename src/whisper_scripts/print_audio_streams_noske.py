import subprocess
import os
import re

def list_language_tracks(file_path):
    # Construct the ffmpeg command to probe the file
    command = [
        'ffmpeg', 
        '-probesize', '50M',          # Increase probesize
        '-analyzeduration', '100M',   # Increase analyzeduration
        '-i', file_path               # Input file
    ]

    # Run the command and capture stderr (where ffmpeg outputs its info)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if ffmpeg ran successfully
    if result.returncode != 0:
        # Parse the output to find language tracks
        lines = result.stderr.decode().split('\n')
        for line in lines:
            if 'Stream' in line and 'Audio' in line and ('eng' in line or 'fr' in line or 'ita' in line or 'slv' in line):
                print(line)

# Replace with your video file path
file_path = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\videos_all_languages\\0059.wmv'

list_language_tracks(file_path)

import os
import pandas as pd
import requests
import subprocess
import re

def download_file(url, local_filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        print(f"Downloaded video to {local_filename}")
        return local_filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def extract_audio(video_file, start_time, end_time, output_file):
    command = [
        'ffmpeg',
        '-i', video_file,
        '-ss', start_time,
        '-to', end_time,
        '-c:a', 'libmp3lame',
        '-q:a', '2',
        '-y',  # Overwrite output files without asking
        output_file
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error in audio extraction: {result.stderr.decode()}")
    else:
        print(f"Audio extracted to {output_file}")

def parse_video_details(s_video):
    match = re.search(r"http://amelia.sslmit.unibo.it/video/video.php\?id=([^&]+)&start=([^&]+)&end=([^&]+)", s_video)
    if match:
        video_id = match.group(1)
        start_time = match.group(2)
        end_time = match.group(3)
        video_url = f"http://amelia.sslmit.unibo.it/video/{video_id}.mp4"
        return video_url, start_time, end_time
    else:
        print(f"Could not parse video details from {s_video}")
        return None, None, None

# Main directories
main_dirs = ['E:/Code/eptic/data/raw/noske_videos/video_audios/slovenian']

for main_dir in main_dirs:
    for subfolder in os.listdir(main_dir):
        subfolder_path = os.path.join(main_dir, subfolder)
        if os.path.isdir(subfolder_path):
            # Find the .xlsx file in the subfolder
            for file in os.listdir(subfolder_path):
                if file.endswith('.xlsx'):
                    xlsx_path = os.path.join(subfolder_path, file)
                    df = pd.read_excel(xlsx_path)

                    # Process each row for audio extraction
                    for index, row in df.iterrows():
                        video_url, start_time, end_time = parse_video_details(row['s.video'])
                        if video_url:
                            # Extract s.id after the colon
                            s_id = row['s.id'].split(':')[-1] if ':' in str(row['s.id']) else row['s.id']
                            audio_filename = f"{row['text.id']}_{s_id}_{row['subset']}.mp3"
                            video_file_path = os.path.join(subfolder_path, f'video_{index}.mp4')
                            output_mp3 = os.path.join(subfolder_path, audio_filename)
                            
                            # Download the video file
                            downloaded_video = download_file(video_url, video_file_path)
                            if downloaded_video:
                                # Extract the audio segment
                                extract_audio(video_file_path, start_time, end_time, output_mp3)
                                
                                # Remove the downloaded video file
                                os.remove(video_file_path)
                        else:
                            print(f"Skipping row {index} due to missing video details.")

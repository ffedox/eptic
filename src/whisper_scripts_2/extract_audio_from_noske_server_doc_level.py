import os
import pandas as pd
import requests
import subprocess
import re

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
        '-y',
        output_file
    ]
    subprocess.run(command)

def parse_video_details(s_video):
    match = re.search(r"http://amelia.sslmit.unibo.it/video/video.php\?id=([^&]+)&start=([^&]+)&end=([^&]+)", s_video)
    if match:
        video_id = match.group(1)
        start_time = match.group(2)
        end_time = match.group(3)
        video_url = f"http://amelia.sslmit.unibo.it/video/{video_id}.mp4"
        return video_url, start_time, end_time
    return None, None, None

main_dir = 'E:/Code/eptic/data/raw/noske_videos/video_audios/english'
test_dir = os.path.join(main_dir, 'dev')
full_dir = os.path.join(test_dir, 'full')
if not os.path.exists(full_dir):
    os.makedirs(full_dir)

for file in os.listdir(test_dir):
    if file.endswith('.xlsx'):
        xlsx_path = os.path.join(test_dir, file)
        df = pd.read_excel(xlsx_path)
        grouped_df = df.groupby('text.id')

        for text_id, group in grouped_df:
            first_video_url, first_start_time, _ = parse_video_details(group.iloc[0]['s.video'])
            _, _, last_end_time = parse_video_details(group.iloc[-1]['s.video'])

            if first_video_url:
                audio_filename = f"{text_id}.mp3"
                video_file_path = os.path.join(test_dir, f'video_{text_id}.mp4')
                output_mp3 = os.path.join(full_dir, audio_filename)

                downloaded_video = download_file(first_video_url, video_file_path)
                if downloaded_video:
                    extract_audio(video_file_path, first_start_time, last_end_time, output_mp3)
                    os.remove(video_file_path)

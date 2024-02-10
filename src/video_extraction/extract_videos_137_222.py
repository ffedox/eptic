import pandas as pd
import subprocess
from datetime import datetime
import os

def download_video_segment(event_id, video_url, m3u8_url, output_dir="E:\\Code\\eptic\\src\\video_extraction\\videos"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract and parse start and end times from video_url, handling unexpected content
    start_time_str = video_url.split('&playerStartTime=')[1].split('&')[0]
    end_time_str = video_url.split('&playerEndTime=')[1].split('&')[0]  # Adjusted to ensure no extra content is included
    
    # Attempt to parse the datetime, catching any errors
    try:
        start_datetime = datetime.strptime(start_time_str, "%Y%m%d-%H:%M:%S")
        end_datetime = datetime.strptime(end_time_str, "%Y%m%d-%H:%M:%S")
    except ValueError as e:
        print(f"Error parsing datetime for event_id {event_id}: {e}")
        return  # Skip this row if the datetime format is incorrect
    
    # Extract and parse the stream start time from m3u8_url
    # Assuming the stream start time needs to be handled similarly
    stream_start_str = m3u8_url.split('start=')[1].split('&')[0]
    stream_start_datetime = datetime.strptime(stream_start_str, "%Y-%m-%dT%H:%M:%S+0000")

    # Calculate offsets and duration
    offset_seconds = (start_datetime - stream_start_datetime).total_seconds()
    duration_seconds = (end_datetime - start_datetime).total_seconds() + 5  # Adding 5 seconds buffer

    # Define output file path
    output_file_path = os.path.join(output_dir, f"{event_id}.mp4")
    
    # Construct ffmpeg command
    ffmpeg_command = [
        "ffmpeg",
        "-fflags", "+genpts",
        "-i", m3u8_url,
        "-ss", str(offset_seconds),
        "-t", str(duration_seconds),
        "-map", "0",
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        output_file_path
    ]
    
    # Execute the ffmpeg command
    subprocess.run(ffmpeg_command)
    print(f"Attempted to download video segment for event_id {event_id}.")

# Load the Excel file
df = pd.read_excel("E:\\Code\\eptic\\src\\video_extraction\\137-222_with_video_url_only.xlsx").head(2)  # Limiting to the first 2 rows for testing

# Iterate through the DataFrame and download each video segment
for index, row in df.iterrows():
    download_video_segment(row['event_id'], row['timestamps_url'], row['video_url'])

print("Download of the first 2 video segments attempted.")

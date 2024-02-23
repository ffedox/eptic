import pandas as pd
import subprocess
from datetime import datetime, timedelta
import os

def download_video_segment(event_id, video_url, stream_start_time, m3u8_url, correction_offset_seconds=0):
    # Ensure no leading/trailing whitespaces
    video_url = video_url.strip()
    stream_start_time = stream_start_time.strip()
    m3u8_url = m3u8_url.strip()
    
    # Extract the timestamps from the URL
    start_time_str = video_url.split('&playerStartTime=')[1].split('&')[0].split('-')[1]
    end_time_str = video_url.split('&playerEndTime=')[1].split('-')[1]
    
    # Convert timestamps to datetime objects, ensuring to strip any potential whitespace
    stream_start = datetime.strptime(stream_start_time, "%H:%M:%S")
    desired_start = datetime.strptime(start_time_str, "%H:%M:%S")
    desired_end = datetime.strptime(end_time_str, "%H:%M:%S")

    # Add 5 seconds to the desired_end timestamp
    desired_end += timedelta(seconds=5)

    # Apply a correction offset
    correction_offset = timedelta(seconds=correction_offset_seconds)
    desired_start -= correction_offset
    desired_end -= correction_offset

    # Calculate offset and duration
    offset_seconds = (desired_start - stream_start).total_seconds()
    duration_seconds = (desired_end - desired_start).total_seconds()

    # Ensure the videos directory exists
    output_dir = "E:\\Code\\eptic\\src\\video_extraction\\videos3"
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f"{event_id}.mp4")

    # Construct the ffmpeg command to include all streams
    ffmpeg_command = [
        "ffmpeg",
        "-i", m3u8_url,
        "-ss", str(int(offset_seconds)),
        "-t", str(int(duration_seconds)),
        "-map", "0:v:0",  # Include the video stream
        "-map", "0:a:m:language:eng",  # Include English audio stream
        "-map", "0:a:m:language:fre",  # Include French audio stream
        "-map", "0:a:m:language:ita",  # Include Italian audio stream
        "-map", "0:a:m:language:slv",  # Include Slovenian audio stream
        "-c:v", "copy",  # Copy video codec
        "-c:a", "aac",  # Transcode audio to AAC
        "-v", "verbose",  # Increase verbosity for detailed output
        output_file_path
    ]

    # Execute the ffmpeg command
    subprocess.run(ffmpeg_command)
    print(f"Downloaded video segment for event_id {event_id} to {output_file_path}")

# Load the Excel file
excel_file_path = "E:\\Code\\eptic\\src\\video_extraction\\137-222_with_start_time.xlsx"
df = pd.read_excel(excel_file_path)

# Convert event_id to str and strip whitespaces, then convert to int for comparison
df['event_id'] = df['event_id'].astype(str).str.strip().astype(int)

# Filter the DataFrame to include only rows with event_id >= 141
filtered_df = df[df['event_id'] >= 139]

# Process every row in the filtered DataFrame
for index, row in filtered_df.iterrows():
    download_video_segment(str(row['event_id']), row['timestamps_url'].strip(), row['start_time'].strip(), row['video_url'].strip(), 1)
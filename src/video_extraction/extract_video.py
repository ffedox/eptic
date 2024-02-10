import subprocess
from datetime import datetime, timedelta

# Function to extract timestamps and download the video segment with all streams
def download_video_segment(video_url, stream_start_time, m3u8_url, correction_offset_seconds=0):
    # Extract the timestamps from the URL
    start_time_str = video_url.split('&playerStartTime=')[1].split('&')[0].split('-')[1]
    end_time_str = video_url.split('&playerEndTime=')[1].split('-')[1]

    # Convert timestamps to datetime objects
    stream_start = datetime.strptime(stream_start_time, "%H:%M:%S")
    desired_start = datetime.strptime(start_time_str, "%H:%M:%S")
    desired_end = datetime.strptime(end_time_str, "%H:%M:%S")

    # Add 5 seconds to the desired_end timestamp
    desired_end += timedelta(seconds=5)

    # Apply a correction offset if the video is consistently late by a known amount of seconds
    correction_offset = timedelta(seconds=correction_offset_seconds)
    desired_start -= correction_offset
    desired_end -= correction_offset

    # Calculate offset and duration
    offset_seconds = (desired_start - stream_start).total_seconds()
    duration_seconds = (desired_end - desired_start).total_seconds()

    # Construct the ffmpeg command to include all streams
    ffmpeg_command = [
    "ffmpeg",
    "-i", m3u8_url,
    "-ss", str(int(offset_seconds)),
    "-t", str(int(duration_seconds)),
    "-c", "copy",
    "chunk2.mp4"
]

    # Execute the ffmpeg command
    subprocess.run(ffmpeg_command)

# Example usage:
video_url_example = "https://www.europarl.europa.eu/plenary/en/vod.html?mode=unit&vodLanguage=EN&playerStartTime=20110117-19:19:28&playerEndTime=20110117-19:20:33"
stream_start_time_example = "18:29:40"
m3u8_url_example = "https://manifest.europarl.streaming.arbor.nl/live/201101170900plenary9/index.m3u8?start=2011-01-17T17%3A29%3A40Z&end=2011-01-17T18%3A38%3A50Z&subtitles=1"
correction_offset_seconds_example = 1  # Adjust this value as needed to correct for the delay
download_video_segment(video_url_example, stream_start_time_example, m3u8_url_example, correction_offset_seconds_example)



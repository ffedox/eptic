import subprocess
from datetime import datetime, timedelta

def download_video_segment(video_url, stream_start_time, m3u8_url, correction_offset_seconds=0):
    stream_start = datetime.strptime(stream_start_time, "%H:%M:%S")
    
    start_time_str = video_url.split('&playerStartTime=')[1].split('&')[0]
    end_time_str = video_url.split('&playerEndTime=')[1]
    desired_start = datetime.strptime(start_time_str, "%Y%m%d-%H:%M:%S")
    desired_end = datetime.strptime(end_time_str, "%Y%m%d-%H:%M:%S")

    desired_start = desired_start.replace(year=stream_start.year, month=stream_start.month, day=stream_start.day)
    desired_end = desired_end.replace(year=stream_start.year, month=stream_start.month, day=stream_start.day)

    desired_end += timedelta(seconds=5)

    correction_offset = timedelta(seconds=correction_offset_seconds)
    desired_start -= correction_offset
    desired_end -= correction_offset

    offset_seconds = (desired_start - stream_start).total_seconds()
    duration_seconds = (desired_end - desired_start).total_seconds()

    output_file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_output_with_audio2.mp4"
    ffmpeg_command = [
        "ffmpeg",
        "-fflags", "+genpts",
        "-i", m3u8_url,
        "-ss", str(max(0, offset_seconds)),
        "-t", str(max(0, duration_seconds)),
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        output_file_name
    ]

    subprocess.run(ffmpeg_command)
    print(f"Video segment downloaded to {output_file_name}.")

# Example usage
video_url_example = "https://www.europarl.europa.eu/plenary/en/vod.html?mode=unit&vodLanguage=EN&playerStartTime=20110215-17:38:45&playerEndTime=20110215-17:39:52"
stream_start_time_example = "16:45:33"
m3u8_url_example = "https://manifest.europarl.streaming.arbor.nl/live/201102150900plenary9/199/prog_index.m3u8?start=2011-02-15T11:17:28+0000&end=2011-02-15T12:18:18+0000&sourcetimestamps=1&nocompression=1&returnType=hls"
correction_offset_seconds_example = 1

download_video_segment(video_url_example, stream_start_time_example, m3u8_url_example, correction_offset_seconds_example)
import os
from moviepy.editor import VideoFileClip

def get_video_duration(file_path):
    try:
        with VideoFileClip(file_path) as video:
            return video.duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def calculate_total_duration(folder_path):
    total_duration = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.mp4', '.wmv')):
            file_path = os.path.join(folder_path, file_name)
            duration = get_video_duration(file_path)
            total_duration += duration
    return total_duration

folder_path = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\videos_all_languages'
total_duration_seconds = calculate_total_duration(folder_path)
total_duration_hours = total_duration_seconds / 3600

print(f"Total duration: {total_duration_seconds} seconds ({total_duration_hours} hours)")


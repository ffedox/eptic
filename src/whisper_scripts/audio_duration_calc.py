import os
from pydub import AudioSegment

def calculate_total_duration(directory):
    total_duration = 0

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            file_path = os.path.join(directory, filename)

            # Load the audio file and get its duration
            audio = AudioSegment.from_mp3(file_path)
            total_duration += len(audio)

    # Convert total duration from milliseconds to hours, minutes, and seconds
    total_hours = total_duration // 3600000
    total_minutes = (total_duration % 3600000) // 60000
    total_seconds = (total_duration % 60000) // 1000

    return total_hours, total_minutes, total_seconds

# Path to the directory containing MP3 files
directory = "E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios\\train_en"

# Calculate the total duration
hours, minutes, seconds = calculate_total_duration(directory)
print(f"Total duration: {hours} hours, {minutes} minutes, and {seconds} seconds")

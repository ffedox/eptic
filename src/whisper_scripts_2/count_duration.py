import os
import librosa

def calculate_duration(directory, splits):
    total_duration = 0

    for split in splits:
        split_dir = os.path.join(directory, split)
        if not os.path.exists(split_dir):
            print(f"Directory not found: {split_dir}")
            continue

        for file in os.listdir(split_dir):
            if file.endswith('.mp3'):
                file_path = os.path.join(split_dir, file)
                try:
                    # Load the audio file and get its duration
                    duration = librosa.get_duration(filename=file_path)
                    total_duration += duration
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    return total_duration

# Directory path
directory = "E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios\\dataset\\data"

# Splits to consider
splits = ["train", "test"]

# Calculate total duration
total_duration_seconds = calculate_duration(directory, splits)
total_duration_hours = total_duration_seconds / 3600

print(f"Total duration: {total_duration_hours:.2f} hours")

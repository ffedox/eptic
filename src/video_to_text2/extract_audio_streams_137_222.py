import os
import subprocess

# Define the base directory where the MP4 files and language folders are located
base_dir = "D:\\video\\src\\video_to_text\\5002_5058"

# Define the language codes and their corresponding folder names
languages = {
    'pol': 'pl',
    'eng': 'en'
}

# Iterate through all MP4 files in the base directory
for file in os.listdir(base_dir):
    if file.endswith(".mp4"):
        file_path = os.path.join(base_dir, file)
        
        # For each language, extract the corresponding audio stream
        for lang_code, folder_name in languages.items():
            output_file_name = f"{os.path.splitext(file)[0]}_{folder_name}.mp3"
            output_path = os.path.join(base_dir, folder_name, output_file_name)
            
            # Construct the FFmpeg command for extracting the audio stream
            ffmpeg_command = [
                "ffmpeg",
                "-i", file_path,
                "-map", f"0:m:language:{lang_code}",
                "-vn", "-acodec", "mp3",
                output_path
            ]
            
            # Execute the FFmpeg command
            subprocess.run(ffmpeg_command)

print("Audio extraction completed.")
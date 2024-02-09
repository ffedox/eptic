import shutil
import os

# Define the source and destination directories
source_dir = r"E:\Code\eptic\data\raw\noske_videos\video_audios\english"
destination_dir = "G:\\Il mio Drive\\dataset_en"

# Check if the source directory exists
if not os.path.exists(source_dir):
    print("Source directory does not exist.")
else:
    # Check if the destination directory exists, if not create it
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Copy files from source to destination
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)
        shutil.copy2(source_file, destination_file)  # copy2 to preserve metadata

    print("Files copied successfully.")


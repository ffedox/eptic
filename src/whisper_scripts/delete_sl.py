import os
import shutil

def move_files(src_directory, dest_directory):
    # Check if the source directory exists
    if not os.path.exists(src_directory):
        print(f"Source directory {src_directory} does not exist.")
        return

    # Check if the destination directory exists, create if not
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    # Iterate over all files in the source directory
    for filename in os.listdir(src_directory):
        src_file = os.path.join(src_directory, filename)
        dest_file = os.path.join(dest_directory, filename)

        # Move each file to the destination directory
        shutil.move(src_file, dest_file)
        print(f"Moved file: {filename}")

# Directories
src_directory = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios\\video_audios_slovenian'
dest_directory = 'E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios'

# Run the function
move_files(src_directory, dest_directory)

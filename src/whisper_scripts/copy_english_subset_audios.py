import os
import shutil

# Define the paths
source_train_dir = 'E:/Code/eptic/data/raw/noske_videos/video_audios/train'
source_test_dir = 'E:/Code/eptic/data/raw/noske_videos/video_audios/test'
target_train_dir = 'E:/Code/eptic/data/raw/noske_videos/video_audios/train_en'
target_test_dir = 'E:/Code/eptic/data/raw/noske_videos/video_audios/test_en'

# Create target directories if they don't exist
os.makedirs(target_train_dir, exist_ok=True)
os.makedirs(target_test_dir, exist_ok=True)

# Function to copy files containing 'en' in their names
def copy_files_with_en(source_dir, target_dir):
    for filename in os.listdir(source_dir):
        if 'en' in filename:
            source_path = os.path.join(source_dir, filename)
            target_path = os.path.join(target_dir, filename)
            shutil.copy2(source_path, target_path)

# Copy files for train_en and test_en
copy_files_with_en(source_train_dir, target_train_dir)
copy_files_with_en(source_test_dir, target_test_dir)

"Files containing 'en' in their names have been copied to the respective 'train_en' and 'test_en' directories."
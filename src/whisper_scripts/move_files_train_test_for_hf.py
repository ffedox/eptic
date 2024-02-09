import os
import shutil
import pandas as pd

def move_files(excel_path, target_folder):
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Ensure the target folder exists
    os.makedirs(target_folder, exist_ok=True)

    # Move each file to the target folder
    for file_path in df['audio_file_path']:
        if os.path.isfile(file_path):
            shutil.move(file_path, target_folder)
        else:
            print(f"File not found: {file_path}")

# Define paths
test_excel_path = "E:\\Code\\eptic\\src\\noske_per_whisper\\sentences_noske_cleaned_with_event_id_5_only_found_audios_test.xlsx"
train_excel_path = "E:\\Code\\eptic\\src\\noske_per_whisper\\sentences_noske_cleaned_with_event_id_5_only_found_audios_train.xlsx"
test_folder = "E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios\\test"
train_folder = "E:\\Code\\eptic\\data\\raw\\noske_videos\\video_audios\\train"

# Move files
move_files(test_excel_path, test_folder)
move_files(train_excel_path, train_folder)

print("File transfer completed.")

import pandas as pd
import os
from pathlib import Path

def link_videos_to_excel_polish():
    # Fixed file paths
    final_corpus = 'E:\\Code\\eptic\\src\\noske\\final_corpus_noskeptic.xlsx'
    video_folder = 'E:\\Code\\eptic\\data\\raw\\drive_eptic\\eptic_11_wip\\eptic-plen_inprogress\\videos of Polish speakers at EP'

    # Load the excel file
    df = pd.read_excel(final_corpus)

    # Iterate over video files in the directory
    for video_file in os.listdir(video_folder):
        if video_file.endswith('.mp4'):
            # Extract the first four digits of the video file name
            video_id = video_file.split('.')[0]

            # Construct the full path for the video file
            video_path = str(Path(video_folder) / video_file)

            # Find matching rows in the dataframe and update 'texts.video_url'
            df.loc[df['texts.noske_id'].str.startswith(video_id, na=False), 'texts.video_url'] = video_path

    # Save the modified dataframe back to the Excel file
    df.to_excel(final_corpus, index=False)

# Call the function
link_videos_to_excel_polish()
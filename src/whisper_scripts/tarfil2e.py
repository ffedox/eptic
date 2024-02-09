import tarfile
import os

# Define the path to the .tar.gz file
tar_gz_path = r'D:\Europarl-ASR\Europarl-ASR_v1.0.tar.gz'

# Define the directory where you want to extract the files
extract_to_dir = r'D:\Europarl-ASR'

# Check if the path is a .tar.gz file
if tar_gz_path.endswith('.tar.gz'):
    try:
        # Open the .tar.gz file
        with tarfile.open(tar_gz_path, 'r:gz') as tar:
            # Extract all the contents into the directory
            tar.extractall(path=extract_to_dir)
        print(f"Extraction completed successfully to {extract_to_dir}")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("The specified path does not point to a .tar.gz file.")

import pandas as pd
from datetime import datetime, timedelta
import urllib.parse  # For decoding URL-encoded strings

def extract_and_adjust_start_time(url):
    # Extract the start time from the URL
    start_time_encoded = url.split('start=')[1].split('&')[0]
    # Decode the URL-encoded start time
    start_time_str = urllib.parse.unquote(start_time_encoded)
    # Remove the timezone information (Z) and convert it to a datetime object
    start_time_str = start_time_str.split('T')[1].split('+')[0].replace('Z', '')  # Updated to remove 'Z'
    start_time = datetime.strptime(start_time_str, '%H:%M:%S')
    # Add one hour to the time
    adjusted_start_time = (start_time + timedelta(hours=1)).time()
    # Return the adjusted start time as a string
    return adjusted_start_time.strftime('%H:%M:%S')

# Load the Excel file
excel_file_path = "E:\\Code\\eptic\\src\\video_extraction\\137-222_with_adapted_video_url.xlsx"
df = pd.read_excel(excel_file_path)

# Apply the function to the "video_url" column to create the "start_time" column
df['start_time'] = df['video_url'].apply(extract_and_adjust_start_time)

# Save the updated DataFrame to a new Excel file
new_excel_file_path = "E:\\Code\\eptic\\src\\video_extraction\\137-222_with_start_time.xlsx"
df.to_excel(new_excel_file_path, index=False)

print("Added 'start_time' column and saved to new Excel file.")

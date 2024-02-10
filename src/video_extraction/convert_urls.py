import pandas as pd
import re

def adapt_url(url):
    # Use regex to remove the variable '/{number}/prog_index' part
    base_url = re.sub(r'/\d+/prog_index', '/index', url.split('?')[0])
    
    # Assume the rest of the URL remains the same and needs adjustment for the query parameters
    query_params = url.split('?')[1] if len(url.split('?')) > 1 else ''
    
    # Replace colons and other specific adjustments in query parameters
    query_params = query_params.replace(':', '%3A').replace('+0000', 'Z')
    query_params = query_params.replace('sourcetimestamps=1&nocompression=1&returnType=hls', 'subtitles=1')

    # Reassemble the URL
    adapted_url = f"{base_url}?{query_params}"
    return adapted_url

# Load the Excel file (adjust the file path as necessary)
excel_file_path = "E:\\Code\\eptic\\src\\video_extraction\\137-222_with_video_url_only.xlsx"
df = pd.read_excel(excel_file_path)

# Apply the URL transformation to the "video_url" column
df['video_url'] = df['video_url'].apply(adapt_url)

# Save the modified DataFrame to a new Excel file (adjust the file path as necessary)
new_excel_file_path = "E:\\Code\\eptic\\src\\video_extraction\\137-222_with_adapted_video_url.xlsx"
df.to_excel(new_excel_file_path, index=False)

print("URLs adapted and saved to new Excel file.")

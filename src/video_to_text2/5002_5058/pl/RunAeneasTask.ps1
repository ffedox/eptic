# Define the directory containing your files
$directory = "D:\video\src\video_to_text\5002_5058\pl"

# Get all .mp3 files in the directory
$mp3Files = Get-ChildItem -Path $directory -Filter "*.mp3"

# Loop through each .mp3 file
foreach ($mp3File in $mp3Files) {
    # Extract the event_id from the filename
    $eventID = $mp3File.BaseName -replace "_pl", ""
    
    # Check if the corresponding .txt file exists
    $txtFile = Join-Path $directory "$($eventID)_pl.txt"
    if (Test-Path $txtFile) {
        # Define the output JSON file name
        $outputJsonFile = Join-Path $directory "$($eventID).srt"
        
        # Execute the aeneas task
        python -m aeneas.tools.execute_task $mp3File.FullName $txtFile "task_language=pl|os_task_file_format=srt|is_text_type=plain" $outputJsonFile
    }
}
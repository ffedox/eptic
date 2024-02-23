# Define the directory containing your files
$directory = "D:\video\src\video_to_text\137_222\it"

# Get all .mp3 files in the directory
$mp3Files = Get-ChildItem -Path $directory -Filter "*.mp3"

# Loop through each .mp3 file
foreach ($mp3File in $mp3Files) {
    # Extract the event_id from the filename
    $eventID = $mp3File.BaseName -replace "_it", ""
    
    # Check if the corresponding .txt file exists
    $txtFile = Join-Path $directory "$($eventID)_it.txt"
    if (Test-Path $txtFile) {
        # Define the output JSON file name
        $outputJsonFile = Join-Path $directory "$($eventID).srt"
        
        # Execute the aeneas task
        python -m aeneas.tools.execute_task $mp3File.FullName $txtFile "task_language=ita|os_task_file_format=srt|is_text_type=plain" $outputJsonFile
    }
}
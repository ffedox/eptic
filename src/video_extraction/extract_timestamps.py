import requests
from bs4 import BeautifulSoup

# Prompt the user for a date in year-month-day format
date_input = input("Enter a date in year-month-day format (e.g., 2011-02-15): ")
year, month, day = date_input.split('-')

# Adjust the URL based on the provided date
url_template = "https://www.europarl.europa.eu/doceo/document/CRE-7-{year}-{month}-{day}-TOC_EN.html"
toc_url = url_template.format(year=year, month=month, day=day)

# Ask the user for a section name
section_name = input("Enter the section name (e.g., 'Explanations of vote'): ")

# Use requests to fetch the content of the page
toc_response = requests.get(toc_url)
if toc_response.status_code == 200:
    # Parse the HTML content of the page with BeautifulSoup
    toc_soup = BeautifulSoup(toc_response.text, 'html.parser')
    
    # Find the link to the specified section
    section_link = toc_soup.find('a', string=section_name)
    if section_link:
        # Construct the URL to the section
        section_url = "https://www.europarl.europa.eu" + section_link['href']
        
        # Fetch the content of the section's page
        section_response = requests.get(section_url)
        if section_response.status_code == 200:
            # Ask the user for the speaker's name
            speaker_name = input("Enter the speaker's name (e.g., 'Neelie Kroes'): ")
            
            # Parse the section content
            section_soup = BeautifulSoup(section_response.text, 'html.parser')
            
            # Find the speaker in the section's page and the associated video URL
            speaker_tags = section_soup.find_all('span', string=lambda text: speaker_name in text)
            found = False
            for tag in speaker_tags:
                # Find the nearest preceding anchor tag with a video URL
                video_url_tag = tag.find_previous('a', title="Video of the speeches")
                if video_url_tag and 'href' in video_url_tag.attrs:
                    # Construct the full URL of the speech
                    full_video_url = "https://www.europarl.europa.eu" + video_url_tag['href']
                    print("Video URL of the speech for", speaker_name, ":", full_video_url)
                    found = True
                    break  # Assuming we are looking for the first occurrence

            if not found:
                print(f"Video URL for speaker '{speaker_name}' not found.")
        else:
            print("Failed to fetch the section page. Please check the section URL and try again.")
    else:
        print(f"Section '{section_name}' not found on the page.")
else:
    print("Failed to fetch the table of contents page. Please check the URL and try again.")
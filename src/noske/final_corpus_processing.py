import pandas as pd
import re

def update_noske_id():
    # Open the Excel files
    duplicate_texts_path = 'E:/Code/eptic/src/noske/duplicate_texts.xlsx'
    final_corpus_path = 'E:/Code/eptic/src/noske/final_corpus_noskeptic.xlsx'
    
    duplicate_texts_df = pd.read_excel(duplicate_texts_path)
    final_corpus_df = pd.read_excel(final_corpus_path)

    # Create a new column in final_corpus_df and initialize it with None
    final_corpus_df.insert(2, 'texts.noske_id', None)

    # Iterate through each row in final_corpus_df
    for index, row in final_corpus_df.iterrows():
        text_id = row['texts.id']

        # Check if text_id is an integer
        if isinstance(text_id, int):
            # Check if the value is in the 'id' column of duplicate_texts_df
            if text_id in duplicate_texts_df['id'].values:
                # Find the corresponding value in 'matching_text_id' and assign it
                final_corpus_df.at[index, 'texts.noske_id'] = duplicate_texts_df.loc[duplicate_texts_df['id'] == text_id, 'matching_text_id'].iloc[0]
            # Check if the value is in the 'matching_text_id' column of duplicate_texts_df
            elif text_id in duplicate_texts_df['matching_text_id'].values:
                # Find the corresponding value in 'id' and assign it
                final_corpus_df.at[index, 'texts.noske_id'] = duplicate_texts_df.loc[duplicate_texts_df['matching_text_id'] == text_id, 'id'].iloc[0]

    # Save the updated final_corpus_df back to Excel
    final_corpus_df.to_excel(final_corpus_path, index=False)

    return "Noske ID column updated and saved in final_corpus_noskeptic.xlsx"

def update_non_integer_ids():
    # Open the Excel file
    final_corpus_path = 'E:/Code/eptic/src/noske/final_corpus_noskeptic.xlsx'
    final_corpus_df = pd.read_excel(final_corpus_path)

    # Initialize a counter for the new integer IDs
    new_id = 1150

    # Iterate through each row in final_corpus_df
    for index, row in final_corpus_df.iterrows():
        text_id = row['texts.id']

        # Check if text_id is not exclusively an integer
        if not isinstance(text_id, int):
            # Move the non-integer value to 'texts.noske_id'
            final_corpus_df.at[index, 'texts.noske_id'] = text_id

            # Replace the non-integer value in 'texts.id' with the new integer ID
            final_corpus_df.at[index, 'texts.id'] = new_id

            # Increment the new ID counter
            new_id += 1

    # Save the updated DataFrame back to the Excel file
    final_corpus_df.to_excel(final_corpus_path, index=False)

    return "Non-integer IDs updated in texts.id and texts.noske_id columns."

def append_sentence_split_text():
    # Open the Excel files
    noske_texts_path = 'E:/Code/eptic/docs/noske_texts_with_tags.xlsx'
    final_corpus_path = 'E:/Code/eptic/src/noske/final_corpus_noskeptic.xlsx'
    
    noske_texts_df = pd.read_excel(noske_texts_path)
    final_corpus_df = pd.read_excel(final_corpus_path)

    # Create a new column in final_corpus_df
    final_corpus_df.insert(6, 'texts.noske_sentence_split_text', None)

    # Create a dictionary for faster lookup from noske_texts_df
    id_to_sentence = noske_texts_df.set_index('text.id')['s.text'].to_dict()

    # Iterate through each row in final_corpus_df
    for index, row in final_corpus_df.iterrows():
        noske_id = row['texts.noske_id']

        # Find the corresponding value in noske_texts_df and append it
        if noske_id in id_to_sentence:
            final_corpus_df.at[index, 'texts.noske_sentence_split_text'] = id_to_sentence[noske_id]

    # Save the updated DataFrame back to the Excel file
    final_corpus_df.to_excel(final_corpus_path, index=False)

    return "texts.noske_sentence_split_text column added and updated."

def process_noske_file():

    file_path = 'E:\\Code\\eptic\\src\\noske\\final_corpus_noskeptic.xlsx'

    # Load the excel file
    df = pd.read_excel(file_path)

    # Define the function to extract URLs
    def extract_url_safe(text):
        if isinstance(text, str):
            # Regex pattern to find the URL
            pattern = r'video="(.*?)">'
            # Search for the pattern and extract the URL
            match = re.search(pattern, text)
            # Return the URL if found, else return None
            return match.group(1) if match else None
        else:
            # Return None if the value is not a string
            return None

    # Apply the function to extract URLs
    df['texts.video_url'] = df['texts.noske_sentence_split_text'].apply(extract_url_safe)

    # Insert the new column as the 8th column
    df.insert(7, 'texts.video_url', df.pop('texts.video_url'))

    # Save the modified dataframe to a new file
    # new_file_path = file_path.replace('final_corpus_noskeptic.xlsx', 'modified_corpus_noskeptic.xlsx')
    df.to_excel(file_path, index=False)

    return "Video URLs extracted"

update_noske_id()

update_non_integer_ids()

append_sentence_split_text()

process_noske_file()
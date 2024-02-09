import os
import re
import pandas as pd

def find_matching_files(directory, pattern):
    matching_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if re.match(pattern, file):
                matching_files.append(os.path.join(root, file))
    return matching_files

def extract_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_excel(file_pairs, output_file):
    data = {'tr.orig.txt': [], 'tr.rev.txt': []}
    for orig_file, rev_file in file_pairs:
        data['tr.orig.txt'].append(extract_text(orig_file))
        data['tr.rev.txt'].append(extract_text(rev_file))

    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

def main():
    directory = 'D:/Europarl-ASR/release/en/test/original_audio/spk-dep/speeches'
    orig_pattern = r'.*\.tr\.orig\.txt$'
    rev_pattern = r'.*\.tr\.rev\.txt$'

    orig_files = find_matching_files(directory, orig_pattern)
    rev_files = find_matching_files(directory, rev_pattern)

    file_pairs = []
    for orig_file in orig_files:
        base_name = re.sub(r'\.tr\.orig\.txt$', '', orig_file)
        rev_file = base_name + '.tr.rev.txt'
        if rev_file in rev_files:
            file_pairs.append((orig_file, rev_file))

    if not file_pairs:
        print("No file pairs found. Please check the directory and file patterns.")
        return

    output_file = 'output.xlsx'
    create_excel(file_pairs, output_file)
    print(f"Excel file created with {len(file_pairs)} pairs of files.")

if __name__ == "__main__":
    main()

import json
import os

def flatten_and_clean(filename):
    if not os.path.exists(filename):
        print(f"Skipping {filename}: File not found.")
        return

    with open(filename, 'r') as f:
        data = json.load(f)

    # Flatten logic: if item is a list, take the first element; otherwise keep it
    # Also ensures everything is uppercase and stripped of whitespace
    clean_list = []
    for item in data:
        if isinstance(item, list) and len(item) > 0:
            clean_list.append(str(item[0]).strip().upper())
        elif isinstance(item, str):
            clean_list.append(item.strip().upper())

    with open(filename, 'w') as f:
        json.dump(clean_list, f)
    print(f"Successfully cleaned {filename}!")

# Update these paths to match your local data folder
data_files = ['data/answerlist.json', 'data/wordlist.json', 'data/usedlist.json']

for file in data_files:
    flatten_and_clean(file)

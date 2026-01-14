import pandas as pd
import json
import os

# Assuming your CSV files are in the same directory
# If not, update the paths

# Convert answerlist.csv
try:
    answer_df = pd.read_csv('answerlist.csv')
    answer_list = answer_df.iloc[:, 0].tolist()
    with open('api/wordle/data/answerlist.json', 'w') as f:
        json.dump(answer_list, f)
    print("✓ Created answerlist.json")
except FileNotFoundError:
    print("⚠ answerlist.csv not found. Creating sample data...")
    sample_answers = ["apple", "brave", "crane", "drake", "elate", "frame", "grape", "house", "irate", "jolly"]
    with open('api/wordle/data/answerlist.json', 'w') as f:
        json.dump(sample_answers, f)

# Convert wordlist.csv
try:
    word_df = pd.read_csv('wordlist.csv')
    word_list = word_df.iloc[:, 0].tolist()
    with open('api/wordle/data/wordlist.json', 'w') as f:
        json.dump(word_list, f)
    print("✓ Created wordlist.json")
except FileNotFoundError:
    print("⚠ wordlist.csv not found. Creating sample data...")
    sample_words = ["crane", "slate", "crate", "trace", "salet", "reast", "soare", "raise", "arise", "irate"]
    with open('api/wordle/data/wordlist.json', 'w') as f:
        json.dump(sample_words, f)

# Convert usedlist.csv
try:
    used_df = pd.read_csv('usedlist.csv')
    used_list = used_df.iloc[:, 2].tolist()
    with open('api/wordle/data/usedlist.json', 'w') as f:
        json.dump(used_list, f)
    print("✓ Created usedlist.json")
except FileNotFoundError:
    print("⚠ usedlist.csv not found. Creating sample data...")
    sample_used = ["apple", "brave", "crane"]
    with open('api/wordle/data/usedlist.json', 'w') as f:
        json.dump(sample_used, f)

print("\n✅ All JSON files created in api/wordle/data/")

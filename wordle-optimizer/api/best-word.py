import json
import math
import os
from http.server import BaseHTTPRequestHandler
from datetime import datetime
import random

class WordleSolver:
    def __init__(self, answer_list, guess_list, used_list):
        self.answer_list = set(answer_list)
        self.used_list = set(used_list)
        self.entropy_scores = {}

    def get_pattern(self, guess, answer):
        pattern = [""] * 5
        guess_chars = list(guess)
        answer_chars = list(answer)

        for i in range(5):
            if guess_chars[i] == answer_chars[i]:
                pattern[i] = "g"
                answer_chars[i] = None
                guess_chars[i] = None

        for i in range(5):
            if guess_chars[i] and guess_chars[i] in answer_chars:
                pattern[i] = "y"
                answer_chars[answer_chars.index(guess_chars[i])] = None
                guess_chars[i] = None

        for i in range(5):
            if not pattern[i]:
                pattern[i] = "-"

        return "".join(pattern)

    def calculate_entropy(self, guess, possible_answers):
        patterns = {}
        for answer in possible_answers:
            pattern = self.get_pattern(guess, answer)
            patterns[pattern] = patterns.get(pattern, 0) + 1

        entropy = 0
        total_answers = len(possible_answers)
        for count in patterns.values():
            probability = count / total_answers
            entropy -= probability * math.log2(probability)

        return entropy

    def find_best_starter(self, sample_size=20):
        remaining_answers = list(self.answer_list - self.used_list)
        
        if not remaining_answers:
            return {"word": "CRANE", "entropy": 5.72}

        # Limit for performance
        if len(remaining_answers) > sample_size:
            remaining_answers = random.sample(remaining_answers, sample_size)

        self.entropy_scores = {}
        for guess in remaining_answers[:10]:  # Test first 10
            self.entropy_scores[guess] = self.calculate_entropy(guess, remaining_answers)

        if not self.entropy_scores:
            return {"word": "CRANE", "entropy": 5.72}

        best_word = max(self.entropy_scores, key=self.entropy_scores.get)
        return {"word": best_word, "entropy": self.entropy_scores[best_word]}

def load_word_lists():
    """
    Load word lists from the data folder in the project root.
    Since this file is in /api/best-word.py, we need to go up one level.
    """
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to project root, then into data/
    # Structure: project-root/api/best-word.py
    #           project-root/data/
    data_dir = os.path.join(current_dir, '..', 'data')
    
    # Convert to absolute path and normalize
    data_dir = os.path.abspath(data_dir)
    
    print(f"Looking for data in: {data_dir}")  # Debug line
    
    # Check if directory exists
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found: {data_dir}")
    
    # List files in directory for debugging
    files = os.listdir(data_dir)
    print(f"Files in data directory: {files}")  # Debug line
    
    # Load the JSON files
    with open(os.path.join(data_dir, 'answerlist.json'), 'r') as f:
        answer_list = json.load(f)
    
    with open(os.path.join(data_dir, 'wordlist.json'), 'r') as f:
        guess_list = json.load(f)
    
    with open(os.path.join(data_dir, 'usedlist.json'), 'r') as f:
        used_list = json.load(f)
    
    print(f"Loaded: {len(answer_list)} answers, {len(guess_list)} guesses, {len(used_list)} used")  # Debug line
    
    return answer_list, guess_list, used_list

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            answer_list, guess_list, used_list = load_word_lists()
            solver = WordleSolver(answer_list, guess_list, used_list)
            best_word_data = solver.find_best_starter()
            
            response = json.dumps({
                "status": "success",
                "best_word": best_word_data,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            # Print error for debugging (will appear in Vercel logs)
            print(f"ERROR: {str(e)}")
            import traceback
            print(traceback.format_exc())
            
            response = json.dumps({
                "status": "error",
                "message": str(e),
                "fallback": {"word": "CRANE", "entropy": 5.72}
            })
        
        self.wfile.write(response.encode())

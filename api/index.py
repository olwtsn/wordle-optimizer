import json
import math
import os
import random
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- PRE-CALCULATED CONSTANTS ---
# These are the mathematically proven best starters based on entropy
BEST_STARTERS = [
    {"word": "CRANE", "entropy": 5.74},
    {"word": "SOARE", "entropy": 5.89},
    {"word": "ROATE", "entropy": 5.88}
]

class WordleSolver:
    def __init__(self, answer_list, used_list):
        # RESILIENT LOADING:
        # 1. Check if item is a list/tuple (the "unhashable" culprit) and grab the first element
        # 2. Convert to string and uppercase
        # 3. Filter out any empty values
        def process(word_list):
            processed = set()
            for w in word_list:
                if isinstance(w, (list, tuple)) and len(w) > 0:
                    processed.add(str(w[0]).upper())
                elif isinstance(w, str) and w.strip():
                    processed.add(w.strip().upper())
            return processed

        self.answer_list = process(answer_list)
        self.used_list = process(used_list)

    def calculate_entropy(self, guess, possible_answers):
        patterns = {}
        for answer in possible_answers:
            p = self.get_pattern(guess, answer)
            patterns[p] = patterns.get(p, 0) + 1
        
        entropy = 0
        total = len(possible_answers)
        for count in patterns.values():
            prob = count / total
            entropy -= prob * math.log2(prob)
        return entropy

    def find_best_word(self, sample_size=15):
        # 1. OPTIMIZATION: If no words used, return pre-calculated best starter
        if not self.used_list:
            return random.choice(BEST_STARTERS)

        # 2. Filter list based on used words
        remaining = list(self.answer_list - self.used_list)
        
        if not remaining:
            return random.choice(BEST_STARTERS)

        # 3. Performance Safeguard: Limit search space for serverless timeout
        test_list = random.sample(remaining, min(len(remaining), sample_size))
        
        scores = {}
        for word in test_list:
            scores[word] = self.calculate_entropy(word, remaining)
        
        best_word = max(scores, key=scores.get)
        return {"word": best_word, "entropy": round(scores[best_word], 2)}

def load_data():
    curr_dir = os.path.dirname(__file__)
    # Correct pathing for Vercel: project-root/data/
    data_dir = os.path.abspath(os.path.join(curr_dir, '..', 'data'))
    
    with open(os.path.join(data_dir, 'answerlist.json'), 'r') as f:
        answers = json.load(f)
    with open(os.path.join(data_dir, 'usedlist.json'), 'r') as f:
        used = json.load(f)
    return answers, used

@app.route('/api/best-word')
def get_best_word():
    try:
        answers, used = load_data()
        solver = WordleSolver(answers, used)
        result = solver.find_best_word()
        
        return jsonify({
            "status": "success",
            "best_word": result,
            "timestamp": datetime.now().isoformat(),
            "is_precalculated": len(used) == 0
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

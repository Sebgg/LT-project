"""
Combine two score sheets with:
$ python3 evaluator.py (combine || -c) <original_data> <data_to_merge>

Run the evaluator with:
$ python3 evaluator.py
"""

import json
import random
from flask import Flask, jsonify, request

class Evaluator_Server():
    languages = list()
    translated = {}
    scores = {}
    score_file_name = "scores.json"
    translation_file_name = "translations.json"

    flask_app = Flask("EvalServer")

    def __init__(self):
        with open(self.translation_file_name, encoding='utf-8-sig') as f:
            self.translated = json.load(f)

        with open(self.score_file_name, encoding='utf-8-sig') as f:
            self.scores = json.load(f)

    @flask_app.route("/dump_json")
    def dump_json(self):
        with open(self.score_file_name, 'w+', encoding='utf-8-sig') as f:
            json.dump(self.scores, f)

    # should be superflous
    @flask_app.route("/combine", methods=["POST"])
    def combine_scores(self):
        with open(self.score_file_name, encoding='utf-8-sig') as f:
            original_data = json.load(f)
        
        new_data = request.scores

        for translator, scores in new_data.items():
            original_data[translator] += scores

        with open(self.score_file_name, 'w+', encoding='utf-8-sig') as f:
            json.dump(original_data, f)
    
    @flask_app.route("/get_translation/<language>")
    def evaluate_translation(self, language):
        sentence_id = random.randint(0, 128)
        translator = random.choice(list(self.translated.keys()))

        sentence = self.translated[translator][sentence_id][language]
        original = self.translated[translator][sentence_id]["original"]

        if sentence != "N/A":
            return jsonify({
                "translation": sentence,
                "original": original,
                "iid": sentence_id,
                "translator": translator,
                "success": True
            })
        else:
            return jsonify({"success": False})

    @flask_app.route("/add_score", methods=["POST"])
    def add_score(self):
        score = request.score
        translator = request.translator
        sentence_id = request.iid
        language = request.language

        self.scores[translator].append({
            "score": score,
            "iid": sentence_id,
            "language": language
        })


def main():
    eva = Evaluator_Server()

if __name__ == "__main__":
    main()
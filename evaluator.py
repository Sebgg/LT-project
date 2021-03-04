"""
1. load translation json file
2. load score json file
3. ask what language(s) the evaluator speaks, commaseparated
4. randomize translated sentences from the applicable languages, evaluation counter
5. save scores to the loaded score json file
"""

"""
Combine two score sheets with:
$ python3 evaluator.py (combine || -c) <original_data> <data_to_merge>

Run the evaluator with:
$ python3 evaluator.py
"""

"""
---------------
original text
---------------
translated text
---------------
score (1...5):
---------------
"""
import json
import random
import sys
import time
from textwrap import wrap
import atexit

class Evaluator():
    languages = list()
    translated = {}
    scores = {}
    score_file_name = "scores.json"
    translation_file_name = "translations.json"

    def __init__(self):
        print("\033c")
        print("Welcome to the translation evaluator!\nIt gives you a random ",\
            "to evaluate in one of the languages you know, then you get the\n",\
            "opportunity to score it from 1 (complete fail) to 5 (perfect).",\
            "\n\nYou can stop the program at any time by pressing Ctrl+c if" \
            " you want to stop your work \n")

        with open(self.translation_file_name, encoding='utf-8-sig') as f:
            self.translated = json.load(f)

        with open(self.score_file_name, encoding='utf-8-sig') as f:
            self.scores = json.load(f)

        lang_temp = input("Write all languages you want to " + \
            "evaluate translation in, separated by a Space." + \
            " End by pressing Enter. \n> ")

        self.languages = lang_temp.lower().split()
        atexit.register(self.exit_handler)
        # Dict -> List -> Dict
        # load json files here
        # ask languages
        
    def exit_handler(self):
        self.dump_json()

    def dump_json(self):
        with open(self.score_file_name, 'w+', encoding='utf-8-sig') as f:
            json.dump(self.scores, f)

    def combine_scores(self, original, new):
        with open(original, encoding='utf-8-sig') as f:
            original_data = json.load(f)
        
        with open(new, encoding='utf-8-sig') as f:
            new_data = json.load(f)

        for translator, scores in new_data.items():
            original_data[translator] += scores

        with open(original, 'w+', encoding='utf-8-sig') as f:
            json.dump(original_data, f)
    
    def evaluate_translations(self):
        while True:
            self.evaluate_translation()
            time.sleep(2)

    def evaluate_translation(self):
        language = random.choice(self.languages)
        sentence_id = random.randint(0, 128)
        translator = random.choice(list(self.translated.keys()))

        sentence = '\n'.join(wrap(self.translated[translator][sentence_id][language], 80))
        original = '\n'.join(wrap(self.translated[translator][sentence_id]["original"], 80))

        if sentence != "N/A":
            print("\033c")
            print("The Sentence:\n"+"="*80)
            print(sentence+"\n"+"="*80)
            print("The Original:\n"+"="*80)
            print(original+"\n"+"="*80)
            score = input("How good is the translation? (1 -> 5)\n> ")
            self.scores[translator].append({
                "score": score,
                "id": sentence_id,
                "language": language
            })
            print(f"That translation was from {translator}!")


def main():
    argvs = list(sys.argv)
    if len(argvs) > 2 and \
        (argvs[1] =="combine" or argvs[1] == "-c"):
        eva = Evaluator()
        eva.combine_scores(argvs[2], argvs[3])
    else:
        eva = Evaluator()
        eva.evaluate_translations()

if __name__ == "__main__":
    main()

"""
1. load translation json file
2. load score json file
3. ask what language(s) the evaluator speaks, commaseparated
4. randomize translated sentences from the applicable languages, evaluation counter
5. save scores to the loaded score json file

Combine two score sheets with:
$ python3 evaluator.py (--combine || -c) <original_data> <data_to_merge>

Show statistics from a json file containing scores:
$ python3 evaluator.py (--statistics || -s) <filename>

Run the evaluator with:
$ python3 evaluator.py
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
    score_file_name = "scores_sebastian.json"
    translation_file_name = "translations.json"
    counter_file_name = "cup.txt"
    counter = 0

    def __init__(self):
        atexit.register(self.exit_handler)
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
            
        with open(self.counter_file_name, 'r', encoding='utf-8') as f:
            temp = f.readline()
            if temp != None and temp != "":
                self.counter = int(temp)

        lang_temp = input("Write all languages you want to " + \
            "evaluate translation in, separated by a Space." + \
            " End by pressing Enter. \n> ")

        self.languages = lang_temp.lower().split()
        
    def exit_handler(self):
        self.save_counter()
        self.dump_json()

    def dump_json(self):
        with open(self.score_file_name, 'w+', encoding='utf-8-sig') as f:
            json.dump(self.scores, f)

    def save_counter(self):
        with open(self.counter_file_name, 'w', encoding='utf-8') as f:
            f.write(str(self.counter))
    
    def evaluate_translations(self):
        while True:
            self.evaluate_translation()
            time.sleep(2)

    def evaluate_translation(self):
        language = random.choice(self.languages)
        
        translator = random.choice(list(self.translated.keys()))
        iid = self.counter%127
        original_lang = self.translated[translator][iid]["original language"]

        if original_lang in self.languages:
            sentence = '\n'.join(wrap(self.translated[translator][iid][language], 80))
            original = '\n'.join(wrap(self.translated[translator][iid]["original"], 80))

            if sentence != "N/A" and self.translated[translator][iid]:
                print("\033c")
                print(f'Evaluation #{self.counter}')
                print("The Translation:\n"+"="*80)
                print(sentence+"\n"+"="*80)
                print("The Original sentence:\n"+"="*80)
                print(original+"\n"+"="*80)
                score = input("How good is the translation? (1 -> 5, 0 to skip the sentence)\n> ")
                if int(score) >= 1:
                    self.scores[translator].append({
                        "score": score,
                        "id": iid,
                        "language": language
                    })
                    print(f"That translation was from {translator}!")
                    self.counter += 1
                elif int(score) < 0:
                    print("Invalid score!")
                    self.counter += 1
        

def combine_scores(original, new):
        with open(original, encoding='utf-8-sig') as f:
            original_data = json.load(f)
        
        with open(new, encoding='utf-8-sig') as f:
            new_data = json.load(f)

        for translator, scores in new_data.items():
            original_data[translator] += scores

        with open(original, 'w+', encoding='utf-8-sig') as f:
            json.dump(original_data, f)

def show_statistics(filename):
    scores = {}
    with open(filename, encoding='utf-8-sig') as f:
        scores = json.load(f)

    for translator, scores in scores.items():
        all_scores = []
        sentences = set()
        for score in scores:
            all_scores.append(int(score["score"]))
            sentences.add(int(score['id']))

        all_scores.sort()
        mean = 0
        if len(all_scores) > 0:
            mean = float(sum(all_scores)/len(all_scores))
        
            print(f'-'*80)
            print(f'Statistics for {translator}:')
            print(f'Mean score: {mean}')
            print(f'Median score: {all_scores[int(len(all_scores)/2)]}')
            print(f'# of evaluations: {len(all_scores)}')
            print(f'Number of unique sentences evaluated: {len(sentences)}')
            print(f'% of original sentences evaluated: {float(129/len(sentences))}')
            print(f'-'*80)


def main():
    argvs = list(sys.argv)
    if len(argvs) >= 2:
        if (argvs[1] =="--combine" or argvs[1] == "-c"):
            combine_scores(argvs[2], argvs[3])
        elif (argvs[1] == "--statistics" or argvs[1] == '-s'):
            show_statistics(argvs[2])
    else:
        eva = Evaluator()
        eva.evaluate_translations()

if __name__ == "__main__":
    main()

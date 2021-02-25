"""
1. load translation json file
2. load score json file
3. ask what language(s) the evaluator speaks, commaseparated
4. randomize translated sentences from the applicable languages, evaluation counter
5. save scores to the loaded score json file
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

class Evaluator():
    languages = list()
    translated = {}
    scores = {}

    def __init__(self):
        # with open('data.json', encoding='utf-8-sig') as f:
        #     data = json.load(f)
        # print(data)
        pass
        # Dict -> List -> Dict
        # load json files here
        # ask languages

    def dump_json():
        pass

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
            do_next = input("Evaluate a text? Y/N: ")
            if do_next == "N" or do_next == "n":
                break
            self.evaluate_translation()

        self.dump_json()
        pass
        # loop here

    def evaluate_translation(self):
        pass
        # single evaluation here

def main():
    argvs = list(sys.argv)
    if argvs[1] =="combine":
        eva = Evaluator()
        eva.combine_scores(argvs[2], argvs[3])
    else:
        eva = Evaluator()
        eva.evaluate_translations()

if __name__ == "__main__":
    main()
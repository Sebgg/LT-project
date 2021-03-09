# Objective evaluation with the Levensteyhn distance
# Tom Könecke 4.3.2021
import sys
import json
import numpy as np

def main():
    argvs = list(sys.argv)
    if len(argvs) != 3:
        print('Usage is: python objective_eval.py <translation file> <objective scores file>')
        return 1

    translation_file_name = argvs[1]
    objective_score_file_name = argvs[2]

    with open(translation_file_name, encoding='utf-8-sig') as f:
        data = json.load(f)

    for translator in data.keys():
        total = 0
        for sentence in data[translator]:
            # get sentences
            original = sentence['original']
            # TODO find out what the original language is, and use that below.
            circle = sentence['english']
            
            # evaluate them
            score = objective_distance(original, circle)

            # add scores
            total += score

        # add total to obective_scores.json
        with open(objective_score_file_name, encoding='utf-8-sig') as f:
            scores = json.load(f)

        scores[translator] = total
        with open(objective_score_file_name, 'w+', encoding='utf-8-sig') as f:
            json.dump(scores, f)


def tokenize_ws(line):
    tokens = []
    for token in line.split():
        tokens.append(token)
    return tokens

def objective_distance(text1, text2):
    """
    Main method for Objective Evaluation.

    Takes two texts as strings, tokenizes by whitespace and calculates the
    Levensteyhn distance and normalizes by sentence length.
    This relies on an implementation found here:
    https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/ 
    Minor adaptions and translation to Python 3.9 was done.
    """
    # whitespace tokenization
    text1 = tokenize_ws(text1)
    text2 = tokenize_ws(text2)

    # Add the '#' to the beginning of the two sentences
    size_x = len(text1) + 1
    size_y = len(text2) + 1

    matrix = np.zeros((size_x, size_y))
    # add first row and column
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    # iteration all cells
    for x in range(1, size_x):
        for y in range(1, size_y):
            if text1[x-1] == text2[y-1]: # if last character is the same
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x, y-1] + 1,
                    matrix[x-1, y-1]
                )
            else: # if last character is not the same
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x, y-1] + 1,
                    matrix[x-1, y-1] + 1
                )

    # return result divided by sentence length
    return matrix[size_x - 1, size_y - 1] / len(text1)

if __name__ == '__main__':
    main()
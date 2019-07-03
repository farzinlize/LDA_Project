import random

'''
any sentences has 2 part: primary and secondary
words between these two part will randomly placed anywhere in sentence

words devided into 4 group related to their score
    words with 0.8 score or above:  high
    words between 0.6 and 0.8:      semi-high
    words between 0.4 and 0.6:      semi-low
    words with 0.4 score or below:  low

types of primary part:
    4 high emotion words + 1 semi-high emotion word     (5 words)
    3 high emotion words + 2 semi-high emotion words    (5 words)
    4 high emotion words                                (4 words)
    3 high emotion words + 1 semi-high emotion word     (4 words)

type of secondary part:
    2 semi-low emotion words                        (2 words)
    1 semi-low emotion word + 1 low emotion word    (2 words)
    1 semi-low emotion word                         (1 word)
    1 low emotion word                              (1 word)
'''

score_category = {"high":0, "semi-high":1, "semi-low":2, "low":3}
primary_category = [[4, 1], [3, 2], [4, 0], [3, 1]]
secondary_category = [[2, 0], [1, 1], [1, 0], [0, 1]]

dataset = {"anger":[[] for i in range(4)], "fear":[[] for i in range(4)], \
    "sadness":[[] for i in range(4)], "joy":[[] for i in range(4)]}

dataset_test = open("dataset-test.txt", "r")
dataset_test.readline()

for line in dataset_test:
    terms = line.split()
    score = float(terms[1])
    if score >= 0.8:
        dataset[terms[2]][score_category["high"]].append(tuple([terms[0], score]))
    elif score >= 0.6:
        dataset[terms[2]][score_category["semi-high"]].append(tuple([terms[0], score]))
    elif score >= 0.4:
        dataset[terms[2]][score_category["semi-low"]].append(tuple([terms[0], score]))
    else:
        dataset[terms[2]][score_category["low"]].append(tuple([terms[0], score]))

dataset_test.close()


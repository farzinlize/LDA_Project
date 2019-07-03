from helper_functions import sentence_toString
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
primary_emotions = ["anger", "fear", "sadness", "joy"]
secondary_emotions = ["anger", "fear", "sadness", "joy"]
primary_category = {"anger":[[4, 1], [3, 2], [4, 0], [3, 1]], "fear":[[4, 1], [3, 2], [4, 0], [3, 1]],\
     "sadness":[[4, 1], [3, 2], [4, 0], [3, 1]], "joy":[[4, 1], [3, 2], [4, 0], [3, 1]]}
secondary_category = {"anger":[[2, 0], [1, 1], [1, 0], [0, 1]], "fear":[[2, 0], [1, 1], [1, 0], [0, 1]],\
     "sadness":[[2, 0], [1, 1], [1, 0], [0, 1]], "joy":[[2, 0], [1, 1], [1, 0], [0, 1]]}

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

generated = open("generated.txt", "w")

while True:
    if len(primary_emotions) == 0 or len(secondary_emotions) == 0:
        break
    primary_emotion = random.choice(primary_emotions)
    secondary_emotion = random.choice(secondary_emotions)
    if primary_emotion == secondary_emotion:
        continue
    primary = random.choice(primary_category[primary_emotion])
    secondary = random.choice(secondary_category[secondary_emotion])

    sentence = []
    for i in range(primary[0]):
        index = random.randint(0, len(dataset[primary_emotion][score_category["high"]])-1)
        sentence += [dataset[primary_emotion][score_category["high"]][index][0]]
        dataset[primary_emotion][score_category["high"]] = dataset[primary_emotion][score_category["high"]][:index] + \
            dataset[primary_emotion][score_category["high"]][index+1:]
    for i in range(primary[1]):
        index = random.randint(0, len(dataset[primary_emotion][score_category["semi-high"]])-1)
        sentence += [dataset[primary_emotion][score_category["semi-high"]][index][0]]
        dataset[primary_emotion][score_category["semi-high"]] = dataset[primary_emotion][score_category["semi-high"]][:index] + \
            dataset[primary_emotion][score_category["semi-high"]][index+1:]
    for i in range(secondary[0]):
        index = random.randint(0, len(dataset[secondary_emotion][score_category["semi-low"]])-1)
        sentence += [dataset[secondary_emotion][score_category["semi-low"]][index][0]]
        dataset[secondary_emotion][score_category["semi-low"]] = dataset[secondary_emotion][score_category["semi-low"]][:index] + \
            dataset[secondary_emotion][score_category["semi-low"]][index+1:]
    for i in range(secondary[1]):
        index = random.randint(0, len(dataset[secondary_emotion][score_category["low"]])-1)
        sentence += [dataset[secondary_emotion][score_category["low"]][index][0]]
        dataset[secondary_emotion][score_category["low"]] = dataset[secondary_emotion][score_category["low"]][:index] + \
            dataset[secondary_emotion][score_category["low"]][index+1:]
    
    generated.write(sentence_toString(sentence, primary_emotion, secondary_emotion))

    if len(dataset[primary_emotion][score_category["high"]]) < 4:
        primary_category[primary_emotion] = [item for item in primary_category[primary_emotion] \
             if item[0] < 4]
    if len(dataset[primary_emotion][score_category["high"]]) < 3:
        primary_emotions = [emotion for emotion in primary_emotions if emotion != primary_emotion]
    if len(dataset[primary_emotion][score_category["semi-high"]]) < 2:
        primary_category[primary_emotion] = [item for item in primary_category[primary_emotion] \
             if item[1] < 2]
    if len(dataset[primary_emotion][score_category["semi-high"]]) < 1:
        primary_category[primary_emotion] = [item for item in primary_category[primary_emotion] \
             if item[1] < 1]
    if len(primary_category[primary_emotion]) == 0:
        primary_emotions = [emotion for emotion in primary_emotions if emotion != primary_emotion]

    if len(dataset[secondary_emotion][score_category["semi-low"]]) < 2:
        secondary_category[secondary_emotion] = [item for item in secondary_category[secondary_emotion] \
            if item[0] < 2]
    if len(dataset[secondary_emotion][score_category["semi-low"]]) < 1:
        secondary_category[secondary_emotion] = [item for item in secondary_category[secondary_emotion] \
            if item[0] < 1]
    if len(dataset[secondary_emotion][score_category["low"]]) < 1:
        secondary_category[secondary_emotion] = [item for item in secondary_category[secondary_emotion] \
            if item[1] < 1]
    if len(secondary_category[secondary_emotion]) == 0:
        secondary_emotions = [emotion for emotion in secondary_emotions if emotion != secondary_emotion]


generated.close()
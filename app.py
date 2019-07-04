from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from gensim.test.utils import datapath
from helper_functions import extraxtWords, query, topicScore
import gensim


def generate_save(filename):
    '''
    read dataset, generate lda model and dictionary and save them to seprated files
        input:
            filename    --> name of the file that lda model should be saved in
        output:
            ldamodel    --> generated model
            dictionary  --> generated dictionary
    '''
    dataset = open("dataset.txt", "r")

    texts = []
    for line in dataset:
        accept = line.split()[-1]
        if accept == "0":
            continue
        tokens = [line.split("--")[0]] + line.split("--")[1].split()[:-1]
        texts.append(tokens)
    
    dataset.close()

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # saving the dictionary in file
    fname_d = datapath("dictionary.txt")
    dictionary.save_as_text(fname_d)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=20)

    # saving the model in file
    fname_m = datapath(filename)
    ldamodel.save(fname_m)

    return ldamodel, dictionary


num_topics = 8
filenames = {8:"ldamodel_8_topic.lda", 10:"ldamodel_10_topic.lda"}

# try to load model and dictionary from file or generate them if could'nt
try:
    fname_m = datapath(filenames[num_topics])
    ldamodel = gensim.models.ldamodel.LdaModel.load(fname_m, mmap='r')
    fname_d = datapath("dictionary.txt")
    dictionary = corpora.Dictionary.load_from_text(fname_d)
    print("model and dictionary readed from file successfully")
except:
    print("generation model and dictionary from dataset")
    ldamodel, dictionary = generate_save(filenames[num_topics])


# print the topics with 10 most related words
for topic in ldamodel.show_topics(num_topics=num_topics, num_words=10):
    print(" | " + str(topic[0]) + " | " + extraxtWords(topic[1]) + " | ")


# make a dictionary to extract and save frequently score of each emotion in each topic
emotions = {"fear":[], "anger":[], "anticip":[], "trust":[], "surprise":[], "positive":[], \
    "negative":[], "sadness":[], "disgust":[], "joy":[]}

for emotion in emotions.keys():
    emotions[emotion] = [topicScore(emotion, i, ldamodel, dictionary) for i in range(num_topics)]
    print(emotion, ":", emotions[emotion])

# ---------- testing part 1 ---------- #
dataset_test = open("dataset-test.txt", "r")
result_file = open("result.txt", "w")
dataset_test.readline()

success_1 = 0   # number of queries with greater score than accept threshold in the most related topic
success_2 = 0   # number of queries with greater score than accept threshold in the second most related topic
fail = 0        # number of queries that dose not satisfy two conditions above
varians = 0     # avrage different between positive success values

accept_threshold = 0.0001

for line in dataset_test:
    terms = line.split()
    if float(terms[1]) < 0.5:
        continue
    macths_list = query(terms[0], ldamodel, dictionary)
    first_related_emotion_score = emotions[terms[-1]][macths_list[0][0]]
    second_related_emotion_score = emotions[terms[-1]][macths_list[1][0]]
    if first_related_emotion_score > accept_threshold:
        success_1 += 1
        varians += float(terms[1]) - first_related_emotion_score
    elif second_related_emotion_score > accept_threshold:
        success_2 += 1
        varians += float(terms[1]) - second_related_emotion_score
    else:
        fail += 1
    result_file.write(str(macths_list[0][1]) + ", " + str(macths_list[1][1]) + "\n")

varians = varians / (success_1 + success_2)

dataset_test.close()
result_file.close()

print("positive emotion value for query in the most related topic: ", success_1)
print("positive emotion value for query in the second most related topic: ", success_2)
print("zero value for query at two first topic: ", fail)
print("avrage different between positive success values: ", varians)


# ---------- testing part 2 ---------- #
dataset_generated = open("generated.txt", "r")

primary_accept_threshold = 0.005
secondary_accept_threshold = 0.001

# primary emotion variables
success_primary_1 = 0   # successful queries with the most related topic
success_primary_2 = 0   # successful queries with the second most related topic
fail_primary = 0        # failed queries

# secondary emotion variables
success_secondary_1 = 0 # successful queries with the most related topic
success_secondary_2 = 0 # successful queries with the second most related topic
fail_secondary = 0      # failed queries

for line in dataset_generated:
    words_emotion = line.split("|")
    macths_list = query(words_emotion[0], ldamodel, dictionary)
    labeled_emotions = words_emotion[1].split()
    primary_emotion = labeled_emotions[0]
    secondary_emotion = labeled_emotions[1]

    first_topic_scores = (emotions[primary_emotion][macths_list[0][0]], \
        emotions[secondary_emotion][macths_list[0][0]])
    second_topic_scores = (emotions[primary_emotion][macths_list[1][0]], \
        emotions[secondary_emotion][macths_list[1][0]])

    # primary query check
    if first_topic_scores[0] > primary_accept_threshold:
        success_primary_1 += 1
    elif second_topic_scores[0] > primary_accept_threshold:
        success_primary_2 += 1
    else:
        fail_primary += 1

    # secondary query check
    if first_topic_scores[1] > secondary_accept_threshold:
        success_secondary_1 += 1
    elif second_topic_scores[1] > secondary_accept_threshold:
        success_secondary_2 += 1
    else:
        fail_secondary += 1


print("Primary Emotion Query:")
print("Number of success on first topic: ", success_primary_1)
print("Number of success on second topic: ", success_primary_2)
print("Fail: ", fail_primary)

print("Secondary Emotion Query:")
print("Number of success on first topic: ", success_secondary_1)
print("Number of success on second topic: ", success_secondary_2)
print("Fail: ", fail_secondary)

dataset_generated.close()
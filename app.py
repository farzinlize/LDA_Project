from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from helper_functions import extraxtWords, query, topicScore
import gensim

dataset = open("dataset.txt", "r")

num_topics = 8

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
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=20)

for topic in ldamodel.show_topics(num_topics=num_topics, num_words=10):
    print(" | " + str(topic[0]) + " | " + extraxtWords(topic[1]) + " | ")

emotions = {"fear":[], "anger":[], "anticip":[], "trust":[], "surprise":[], "positive":[], \
    "negative":[], "sadness":[], "disgust":[], "joy":[]}

for emotion in emotions.keys():
    emotions[emotion] = [topicScore(emotion, i, ldamodel, dictionary) for i in range(num_topics)]
    print(emotion, ":", emotions[emotion])

dataset_test = open("dataset-test.txt", "r")
result_file = open("result.txt", "w")
dataset_test.readline()

success_1 = 0   # positive emotion value for query in the most related topic
success_2 = 0   # positive emotion value for query in the second most related topic
fail = 0        # zero value for query at two first topic
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
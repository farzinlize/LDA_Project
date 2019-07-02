from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from helper_functions import extraxtWords, query, topicScore
import gensim

dataset = open("dataset.txt", "r")

num_topics = 10

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

success = 0
fail = 0
tests_num = 0
varians = 0

for line in dataset_test:
    terms = line.split()
    best_macth = query(terms[0], ldamodel, dictionary)[0]
    related_emotion_score = emotions[terms[-1]][best_macth[0]]
    # print(terms[0], float(terms[1]), related_emotion_score)
    result_file.write(terms[0] + ":" + terms[1] + " --> " + str(related_emotion_score) + "\n")

# query_result = query('hatred', ldamodel, dictionary)
# print(query_result)

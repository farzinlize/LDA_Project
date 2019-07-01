from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from helper_functions import extraxtWords
import gensim

dataset = open("dataset.txt", "r")

texts = []

for line in dataset:
    accept = line.split()[-1]
    if accept == "0":
        continue
    
    tokens = [line.split("--")[0]] + line.split("--")[1].split()[:-1]

    texts.append(tokens)
    
# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=8, id2word = dictionary, passes=20)

for topic in ldamodel.show_topics(num_topics=8, num_words=10):
    print(" | " + str(topic[0]) + " | " + extraxtWords(topic[1]) + " | ")


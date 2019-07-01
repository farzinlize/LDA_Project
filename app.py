from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

def extraxtWords(topicStr):
    lst = topicStr.split('"')
    result = ""
    for i in range(len(lst)):
        if i%2 == 1:
            result += lst[i] + ", "
    return result[:-2]

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
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=20)

for topic in ldamodel.show_topics(num_topics=10, num_words=10):
    print(extraxtWords(topic[1]))
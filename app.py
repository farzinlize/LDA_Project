from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
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
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=20)

ldamodel.show_topics()
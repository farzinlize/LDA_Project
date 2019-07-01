import gensim

emotions = ["fear", "anger", "anticip", "trust", "surprise", "positive", \
    "negative", "sadness", "disgust", "joy"]

def extraxtWords(topicStr):
    lst = topicStr.split('"')
    result = ""
    for i in range(len(lst)):
        if i%2 == 1:
            result += lst[i] + ", "
    return result[:-2]


def extractWordsFrequency(topicStr):
    lst = topicStr.split('"')
    freq_num = 0
    word_freq = []
    for i in range(len(lst)):    
        if i%2 == 0:
            freq = lst[i].split("*")[0].split()
            if len(freq) == 0:
                continue
            else:
                freq_num = float(freq[-1])
        else:
            word_freq.append([freq_num, lst[i]])
    return word_freq


def topicScore(emotion, topicIdx, ldamodel, dictionary):
    topic = ldamodel.show_topics(num_words=len(dictionary))[topicIdx]
    word_freq = extractWordsFrequency(topic[1])
    for entry in word_freq:
        if entry[1] == emotion:
            return entry[0]
    return 0


def query(str, ldamodel, dictionary):

    query = ['furiously']

    id2word = gensim.corpora.Dictionary()
    _ = id2word.merge_with(dictionary)

    query = id2word.doc2bow(query)

    a = list(sorted(ldamodel[query], key=lambda x: x[1]))
    print(a[0])
    print(a[-1])

    ldamodel.print_topic(a[0][0]) #least related
    ldamodel.print_topic(a[-1][0]) #most related
import gensim

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


def query(st, ldamodel, dictionary):
    query = st.split()
    id2word = gensim.corpora.Dictionary()
    _ = id2word.merge_with(dictionary)
    query = id2word.doc2bow(query)
    return list(sorted(ldamodel[query], key=lambda x: x[1], reverse=True))


def pop_list(lst, index):
    return lst[:index] + lst[index+1:]
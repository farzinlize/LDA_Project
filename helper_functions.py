import gensim

def extraxtWords(topicStr):
    '''
    extracting words of topic from lda show topics functions
        input:
            topicStr    --> a string containing words with their scores
        output:
            a string containing only words seprated with comma
    '''
    lst = topicStr.split('"')
    result = ""
    for i in range(len(lst)):
        if i%2 == 1:
            result += lst[i] + ", "
    return result[:-2]


def extractWordsFrequency(topicStr):
    '''
    extracting words with their scores from lda show topics function
        input:
            topicStr    --> a string containing words with their scores
        output:
            a list of pairs (list with two element) of words and their scores
    '''
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
    '''
    extracting a specific word score from the model
        input:
            emotion     --> searching element (string)
            topicIdx    --> index of searching topic
            ldamodel    --> the trained model
            dictionary  --> the dictionary that model trained with
        output:
            score of the emotion in the topic
    '''
    topic = ldamodel.show_topics(num_words=len(dictionary))[topicIdx]
    word_freq = extractWordsFrequency(topic[1])
    for entry in word_freq:
        if entry[1] == emotion:
            return entry[0]
    return 0


def query(st, ldamodel, dictionary):
    '''
    query function to make a related list
        input:
            st          --> string containing words seprated with blank space
            ldamodel    --> trained model
            dictionary  --> the dictionary that model trained with
        output:
            a sorted list of the most related topics
    '''
    query = st.split()
    id2word = gensim.corpora.Dictionary()
    _ = id2word.merge_with(dictionary)
    query = id2word.doc2bow(query)
    return list(sorted(ldamodel[query], key=lambda x: x[1], reverse=True))


def sentence_toString(sentence, primary_emotion, secondary_emotion):
    '''
    makeing a string from words and two emotion. words seprated with one space and
    emotion seprrated from words with a line (|)
        input:
            sentences       --> a list of words
            primary_emotion and secondary_emotion --> emotions
        output:
            a string described abow
        example:
            output --> "word1 word2 word3 word4|emotion1 emotion2"
    '''
    result = ""
    for word in sentence:
        result = result + word + " "
    return result[:-1] + "|" + primary_emotion + " " + secondary_emotion + "\n"

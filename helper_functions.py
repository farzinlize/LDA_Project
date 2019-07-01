import gensim

def extraxtWords(topicStr):
    lst = topicStr.split('"')
    result = ""
    for i in range(len(lst)):
        if i%2 == 1:
            result += lst[i] + ", "
    return result[:-2]


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
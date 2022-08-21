from collections import Counter
import collections
import json
import math
from operator import itemgetter
import time
from matplotlib import pyplot as plt

import numpy as np


class PList:
    def __init__(self) -> None:
        self.postings_list = collections.defaultdict(list)

    def indexing(self):
        with open(r'Phase 1 Indexing/result.txt', 'r', encoding='utf_8') as file:
            data = file.read().split('], [')

        for d in data:
            if not self.duplicate_term(d):
                self.add_posting(d)

        self.add_repeatations()
            
        return self.postings_list


    def duplicate_term(self, token):
        if token.split(',')[0].split('"')[1] in self.postings_list:
            try:
                self.postings_list[token.split(',')[0].split('"')[1]].append(list(map(int,token.split(',')[1:])))
            except:
                pass
                return True
        
        return False

    def add_posting(self, token):
        try:
            self.postings_list[token.split(',')[0].split('"')[1]].append( list(map(int,token.split(',')[1:])))
        except:
            pass

    def get_docID(self, term, position=False):
        with open (r'Phase 1 Indexing/postings.json', 'r', encoding='utf_8') as file:
            data = file.read()
        self.postings_list = json.loads(data)
        if term in self.postings_list:
            if not position:
                return self.postings_list[term][-1]

            return self.postings_list[term][:-1]


    def get_negative_docID(self, term):
        docs = self.get_docID(term)
        result = []
        docID = list(range(0,12201,1))
        if docs is not None:
            docs = [d[0] for d in docs]
            for d in docID:
                if d not in docs:
                    result.append(d)
            return result        
        return docID

    def check_phrase(self, term):
        docs = []
        docID = []
        doID =  []
        terms = term.split('"')[1].split(' ')
        for t in terms:
            docs.append(self.get_docID(t,True))

        for t in terms:
            docID.append(self.get_docID(t))
            print(t)

        c= []
        for d in docID:
            for x in d:
                c.append(x[0])
            doID.append(c)
            c = []
        ##print(doID)
        intersect_docs = set.intersection(*[set(x) for x in doID if x is not None])

        filtered_docs = []

        c = []
        for d in docs:
            for i in d:
                if i[1] in intersect_docs:
                    print(i)
                    c.append(i)
            
            filtered_docs.append(c)
       
        res = []
        for i in filtered_docs[0]:
            for j in filtered_docs[1]:
                if i[1] == j[1]:
                    if j[0] - i[0] == 1:
                        res.append(i[1])
        
        print("Filtered", set(res))
        return set(res)

    def add_repeatations(self):
        list = self.postings_list
        for key in list.keys():
            docs = [i[1] for i in list[key]]
            x = Counter(docs)
            list[key].append(x.most_common())
                
def zipfs_law():
    frequency = dict
    with open(r'resultstop.txt', 'r', encoding='utf_8') as file:
        data = file.read().split('], [')
    
    data = [d.split(',')[0].split('"')[1] for d in data]

    counts = collections.Counter(data).most_common()

    top_frequency = counts[0][1]

    zipf_table = []
    for index, item in enumerate(counts, start=1):
        relative_frequency = "1/{}".format(index)
        zipf_frequency = top_frequency * (1 / index)
        difference_actual = item[1] - zipf_frequency
        difference_percent = (item[1] / zipf_frequency) * 100

        zipf_table.append({"word": item[0],
                           "actual_frequency": item[1],
                           "relative_frequency": relative_frequency,
                           "zipf_frequency": zipf_frequency,
                           "difference_actual": difference_actual,
                           "difference_percent": difference_percent})

def heaps_law():
    frequency = dict
    with open(r'result.txt', 'r', encoding='utf_8') as file:
        data = file.read().split('], [')
    file.close()
    data = [d.split(',')[0].split('"')[1] for d in data]
    term_counts = collections.Counter(data).most_common()
    a = []
    for t in term_counts:
        a.append(t[1])
    with open(r'postings.json', 'r', encoding='utf_8') as file:
        tokens = json.load(file)
    file.close()
    token_count = collections.Counter(tokens).most_common()
    b = []
    for t in token_count:
        b.append(t[1])
    try:
        total_tokens = np.log10(a)
        total_terms = np.log10(dtype= b)
        x = np.linspace(0, total_tokens[len(total_tokens) - 1], 2000)
        y = math.log(40, 10) + (1 / 2) * x
        plt.plot(total_tokens, total_terms)
        plt.plot(x, y, '--')
        plt.xlabel('log10 T')
        plt.ylabel('log10 M')
        plt.title('Heap`s law')
        plt.show()
    except:
        pass

if __name__ == '__main__':
    plist = PList()
    s = time.time()
    dict = plist.indexing()
    f = time.time()
    print(f-s)
    
    
 
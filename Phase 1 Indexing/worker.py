from locale import normalize
from select import select
from turtle import pos
from postings import *
from query import *


class Worker():
    def __init__(self) -> None:
        self.docID = []
        self.phrase = []

    def begin_retrieving(self):
        query = Query('افزایش نقدینگی')
        query.parse()

        postings = PList()
        for normal in query.normal:
            print(normal)
            x= postings.get_docID(normal)

            if x is not None:
                self.docID.append(list(p[0] for p in x))
        
        for non in query.negative:
    
            self.docID.append(postings.get_negative_docID(non.split('!')[1]))

        for phrase in query.phrase:
            print(phrase)
            ph = postings.check_phrase(phrase)
            self.docID.append(list(ph))

        result = []
        if self.docID is not None:
            result = set.intersection(*[set(x) for x in self.docID if x is not None])

        print(result)

        with open(r'IR_data.json', 'r', encoding='utf_8') as file:
            data = json.load(file) 
        for i in result:
            print({'No': i,'Title': data[str(i)]['title'],"URL": data[str(i)]['url']})

        file.close()
        

    def get_phrase_docID(self, phrase):
        pass


if __name__ == '__main__':
    query = Worker()
    query.begin_retrieving()
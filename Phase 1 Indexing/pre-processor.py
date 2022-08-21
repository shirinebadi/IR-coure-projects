from lib2to3.pgen2 import token
import time
from tracemalloc import stop
from hazm import Normalizer, word_tokenize, Stemmer, Lemmatizer
import json

class PreProcessor:
    def __init__(self) -> None:
        pass

    def normalize(self, text):
        normalizer = Normalizer()
        normalized = []
        for t in text:
            normalized.append(normalizer.normalize(t))

        return normalized

    def stopwords(self, token):
        stop_words = []
        with open (r'Phase 1 Indexing/stopwords.txt', 'r', encoding='utf_8') as file: 
            stop_words = file.read().splitlines()
        flg = False
        removed = []
        for t in token:
            removed.append(t)
        return removed
    
    def tokenizer(self, text):
        token = []
        for i, te in enumerate(text):
            terms = word_tokenize(te)
            for j,t in enumerate(terms):
                new = [t,j,i]
                token.append(new)

        return token

    def stem(self, token):
        stemmer = Stemmer()
        stemmed = []
        for t in token:
            stemmed.append(stemmer.stem(t))

        return stemmed

    def lemm(self, token):
        lemmatizer = Lemmatizer()
        lemmed = []
        for t in token:
            lemmed.append(lemmatizer.lemmatize(t))

        return lemmed

    def process_json(self, json):
        str = []
        for i in range(0, 12201):
            str.append(''.join(json['{}'.format(i)]['content']))

        return str

if __name__ == '__main__' : 
    with open(r'Phase 1 Indexing/IR_data.json', 'r', encoding='utf_8') as file:
        data = json.load(file) 

    pre_processor = PreProcessor()

    text = pre_processor.process_json(data)
    normalized_text = pre_processor.normalize(text=text)

    stemmed = pre_processor.stem(normalized_text)
    lemmed = pre_processor.lemm(stemmed)
    tokens =  pre_processor.tokenizer(lemmed)

    removed = pre_processor.stopwords(token=tokens)
    s = time.time()
    with open (r'Phase 1 Indexing/result.txt', 'a', encoding='utf_8') as file:
        json.dump([ob for ob in removed], file)
    f = time.time()

    print(f-s)

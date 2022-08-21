import re

class Query():
    def __init__(self, string):
        self.query = string
        self.negative = []
        self.phrase = []
        self.normal = []

    def parse(self):

        for non in re.finditer('[!]\w*', self.query):
            self.negative.append(non.group())
        
        for phrase in re.finditer('"([^"]*)"', self.query):
            self.phrase.append(phrase.group())

        words = self.query.split(' ')
        self.normal = [w for w in words if w not in (n for n in self.negative)]
        self.normal = [normal for normal in self.normal if normal not in (p for p in self.phrase)]


if __name__ == '__main__':

    query = Query('افزایش نقدینگی')
    query.parse()
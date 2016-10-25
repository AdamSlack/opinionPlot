import nltk

class CVProcessor:

    def __init__(self, fileName):
        self.names = self.readData(fileName)
        self.CVs = [CV(n, self.readCV(n)) for n in self.names]

    def readData(self, fileName):
        f = open(fileName)
        return [l.split(" ")[0] for l in f]

    def readCV(self, name):
        f = open("cvs/"+ name +".txt", encoding='UTF-8')
        raw = f.read()
        tokens = nltk.word_tokenize(raw)
        tokens = [w.lower() for w in tokens]
        return nltk.Text(tokens)


class CV:

    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.wordCount = len(text)
        self.iCount = text.count("i")

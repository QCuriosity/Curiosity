import re
class analyser:
    def __init__(self, sentences = []):
        self.sentences = sentences
        self.wordRate = {}

    def rmvSpecilChar(self, sentence, specilChar):
        for ch in specilChar:
            sentence = sentence.replace(ch, ' ')
        return sentence

    def splitSentenceToWords(self, sentence):
        for i in xrange(len(sentence)):
            if ord(sentence[i]) > 127:
                return

        wordList = re.findall("[a-z#+]+", sentence.lower())
        for w in wordList:
            if w in self.wordRate:
                self.wordRate[w] += 1
            else:
                self.wordRate[w] = 1

    def splitAllSentences(self):
        for s in self.sentences:
            self.splitSentenceToWords(s)

    def addAnalysisSentence(self, sentence):
        self.splitSentenceToWords(sentence)

    def test():
        return

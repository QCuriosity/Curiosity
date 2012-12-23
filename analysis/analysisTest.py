from analysis import * 

sentences = ["I'm wan jiadong", "My name is &er sjf", "He name is aa%aa"]
ana = analysis(sentences)

ana.splitAllSentences()

print ana.wordRate

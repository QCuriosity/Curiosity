from analysis import * 
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect('localhost', 'root', 'password', 'test', charset = 'utf8')
cur = db.cursor()

query = "SELECT text FROM statuses"
cur.execute(query)
rows = cur.fetchall()
sentences = []
for r in rows:
    if (type(r[0]) == type(u' ')):
        sentences.append(r[0])
    
ana = analysis(sentences)

ana.splitAllSentences()

print ana.wordRate

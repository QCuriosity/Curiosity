from analysis import * 
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect('localhost', 'root', 'password', 'test', charset = 'utf8')
cur = db.cursor()

query = "SELECT text FROM statuses"
cur.execute(query)
numrow = int(cur.rowcount)
ana = analysis()
for r in xrange(numrow):
    if (type(r[0]) == type(u' ')):
        ana.addAnalysisSentence(r[0])
    


print ana.wordRate

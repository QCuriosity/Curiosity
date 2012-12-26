from analysis import * 
import MySQLdb
import sys
import io

reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect('localhost', 'root', 'password', 'curiosity', charset = 'utf8')
cur = db.cursor()

query = "SELECT text FROM status_t"
#query = "SELECT text FROM status_t limit 0, 10000"
cur.execute(query)
numrow = int(cur.rowcount)
ana = analysis()
for i in xrange(numrow):
    r = cur.fetchone()
    if (type(r[0]) == type(u' ')):
        ana.addAnalysisSentence(r[0])
db.close()
    
f = io.open('result3', 'w')
for k in ana.wordRate.keys():
    f.write(k + ': ' + str(ana.wordRate[k]) + '\n')

f.close()

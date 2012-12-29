import sys
sys.path.append("../database")
from mysql import *
from analysis import * 
import MySQLdb
import io

reload(sys)
sys.setdefaultencoding('utf-8')

host = 'localhost'
user = 'root'
passwd = 'password'
db = 'curiosity'

db = mysql(host, user, passwd, db)
db.connect()

year = 2007
yearCount = 6
monthList = []
for y in xrange(yearCount):
    for m in xrange(1, 13):
        pattern = "%d-%d-01" % (year+y, m)
        monthList.append(pattern)


for m in monthList:
    ana = analysis()
    for r in db.getMonthlyData(m):
        if (type(r[0]) == type(u' ')):
            ana.addAnalysisSentence(r[0])
    for k in ana.wordRate.keys():
        db.saveMonthlyData(k, str(ana.wordRate[k]), m) 
    print "%s done!" % m
        

db.close()

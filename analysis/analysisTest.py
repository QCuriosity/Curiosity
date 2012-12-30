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
dbName = 'curiosity'


year = 2010
yearCount = 6
monthList = []
for y in xrange(yearCount):
    for m in xrange(1, 13):
        if y == 2010 and m <=10:
            continue
        pattern = "%d-%d-01" % (year+y, m)
        monthList.append(pattern)


for m in monthList:
    ana = analysis()
    db = mysql(host, user, passwd, dbName)
    db.connect()
    for r in db.getMonthlyData(m):
        if (type(r[0]) == type(u' ')):
            ana.addAnalysisSentence(r[0])
    for k in ana.wordRate.keys():
        db.saveMonthlyData(k, str(ana.wordRate[k]), m) 
    db.close()
    print "%s done!" % m

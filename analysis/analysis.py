import sys
sys.path.append("../database/")
from mysql import *
from analyser import *
import MySQLdb
import io

reload(sys)
sys.setdefaultencoding('utf-8')

def generateDateList(startYear, count):
    monthList = []
    for y in xrange(count):
        for m in xrange(1, 13):
            pattern = "%d-%d-01" % (startYear+y, m)
            monthList.append(pattern)
    return monthList

monthList = generateDateList(2006, 9)

for m in monthList:
    ana = analyser()
    db = mysql(host, user, passwd, dbName)
    db.connect()
    print "processing %s data..." % m
    for r in db.getMonthlyData(m):
        if (type(r[0]) == type(u' ')):
            ana.addAnalysisSentence(r[0])
    for k in ana.wordRate.keys():
        try:
            db.insertKeyword2DB(k, str(ana.wordRate[k]), m)
        except:
            continue
    db.close()

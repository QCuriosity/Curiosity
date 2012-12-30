import sys
sys.path.append("../database")
from mysql import *
import pylab

def generateDateList(startYear, count):
    monthList = []
    for y in xrange(count):
        for m in xrange(1, 13):
            pattern = "%d-%d-01" % (startYear+y, m)
            monthList.append(pattern)
    return monthList

monthList = generateDateList(2006, 7)

host = '10.30.154.216'
user = 'curiosity'
passwd = 'password'
dbName = 'curiosity'

db = mysql(host, user, passwd, dbName)
db.connect()

print monthList
allCount = []
for m in monthList:
    rows = db.getMonthlyKeywordCount('python', m)
    print rows
    if rows == ():
        allCount.append(0)
    else:
        allCount.append(int(rows[0][0]))
db.close()

title = "2012 python trend"
pylab.plot(range(1, len(allCount)+1), allCount)
pylab.title(title)
pylab.legend(('count', 'month'))
##pylab.xlabel(100)
##pylab.ylabel(100)
pylab.show()
import sys
sys.path.append("../database/")
from mysql import *
import pylab

def generateDateList(startYear, count):
    monthList = []
    for y in xrange(count):
        for m in xrange(1, 13):
            pattern = "%d-%d-01" % (startYear+y, m)
            monthList.append(pattern)
    return monthList

monthList = generateDateList(2011, 2)

host = '10.30.154.216'
user = 'curiosity'
passwd = 'password'
dbName = 'curiosity'



keywords = ['python', 'php', 'c++', 'c#', 'java', 'javascript', 'perl']



def plotMonthlyTrend(keywords, title, monthList):
    db = mysql(host, user, passwd, dbName)
    db.connect()
    allKeywordTrend = []
    for k in keywords:
        allCount = []
        for m in monthList:
            rows = db.getMonthlyKeywordCount(k, m)
            print rows
            if rows == ():
                allCount.append(0)
            else:
                allCount.append(int(rows[0][0]))
            print db.getMonthlyTweetCount(m)
        allKeywordTrend.append(allCount)
    db.close()

    for p in allKeywordTrend:
        pylab.plot(range(1, len(p)+1), p)
    pylab.title(title)
    pylab.legend(keywords)
    pylab.xlabel("month")
    pylab.ylabel("frequency of occurrence")
    pylab.show()

plotMonthlyTrend(keywords, "programming language trend", monthList)

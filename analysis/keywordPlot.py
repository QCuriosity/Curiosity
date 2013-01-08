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

monthList = generateDateList(2010, 2)

host = '10.30.154.216'
user = 'curiosity'
passwd = 'password'
dbName = 'curiosity'

def plotMonthlyTrend(keywords, title, monthList):
    db = mysql(host, user, passwd, dbName)
    db.connect()
    allKeywordTrend = []
    for k in keywords:
        allCount = []
        for m in monthList:
            rows = db.getMonthlyKeywordCount(k, m)
            print rows
            count = 0
            for r in rows:
                count += r[0]
            persent = count*1.0
            cc = db.getMonthlyTweetCount(m)
            if cc == 0:
                persent = 0.0
            else:
                persent /= cc
            allCount.append(persent)
        allKeywordTrend.append(allCount)
    db.close()

    for p in allKeywordTrend:
        pylab.plot(range(1, len(p)+1), p)
    pylab.title(title)
    pylab.legend(keywords)
    pylab.xlabel("month")
    pylab.ylabel("frequency of occurrence")
    pylab.show()

def saveMonthlyTweetCount(monthList):
    db = mysql(host, user, passwd, dbName)
    db.connect()
    for m in monthList:
        db.computeAndSaveMonthlyTweetCount(m)
    db.close()

languageKeywords = ['python', 'c#', 'c++', 'basic', 'java', 'ada', 'matlab', 'lua', 'assembly', 'lisp', 'ruby', 'perl', 'bash', 'fortran']
companyKeywords = ['dell', 'microsoft', 'google', 'apple', 'amazon', 'facebook', 'twitter', 'ibm', 'hp']
#keywords =['the']

#saveMonthlyTweetCount(monthList)
#plotMonthlyTrend(languageKeywords, "programming language trend", monthList)
plotMonthlyTrend(companyKeywords, "company keyword trend", monthList)


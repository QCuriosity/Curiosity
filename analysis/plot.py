from keywordPlot import *

languageKeywords = ['python', 'c#', 'c++', 'basic', 'java', 'lua', 'assembly', 'lisp', 'ruby', 'perl', 'fortran']
companyKeywords = ['dell', 'microsoft', 'google', 'apple', 'amazon', 'facebook', 'twitter', 'ibm', 'hp']
electionKeywords =['obama', 'Romney']

monthList = generateDateList(2011, 2)

plotMonthlyTrend(languageKeywords, "programming language 2011-2012 trend", monthList)
plotMonthlyTrend(companyKeywords, "companies 2011-2012 trend", monthList)
plotMonthlyTrend(electionKeywords, "election 2011-2012 trend", monthList)
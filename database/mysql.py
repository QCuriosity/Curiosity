import MySQLdb
import io


class mysql:
    def __init__(self, host, userName, passwd, dbName, charset = 'utf8'):
        self.host = host
        self.userName = userName
        self.passwd = passwd
        self.dbName = dbName
        self.charset = charset
        self.logfile = io.open("mysql.log", 'a')

    def connect(self):
        self.con = MySQLdb.connect(self.host, self.userName, self.passwd, self.dbName, charset = self.charset)
        self.cur = self.con.cursor()

    def close(self):
        self.con.close()
        self.logfile.close()

    def getMonthlyData(self, month):
        query = "select text from status_t where DATE_FORMAT(created_at, '%%Y-%%m')=DATE_FORMAT('%s', '%%Y-%%m')" % month
        try:
            self.cur.execute(query)
        except MySQLdb.Error, e:
            err = "getMonthlyData() saveMonthlyData() Error %d: %s\n" % (e.args[0], e.args[1]) 
            self.file.write(err)
        numrow = int(self.cur.rowcount)
        for i in xrange(numrow):
            r = self.cur.fetchone()
            yield r
        
    def saveMonthlyData(self, keyword, count, date):
        insert = "insert into monthlyAnalysis(keyword, count, date) value('%s', %s, '%s')" % (keyword, count, date)
        try:
            self.cur.execute(insert) 
            self.con.commit()
        except MySQLdb.Error, e:
            err = "saveMonthlyData() Error %d: %s\n" % (e.args[0], e.args[1]) 
            self.file.write(err)

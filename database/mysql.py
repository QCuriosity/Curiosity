import MySQLdb
import io
import time


class mysql:
    def __init__(self, host, userName, passwd, dbName, charset = 'utf8'):
        self.host = host
        self.userName = userName
        self.passwd = passwd
        self.dbName = dbName
        self.charset = charset
        self.logfile = open("../logs/mysql.log", 'a')

    def connect(self):
        self.con = MySQLdb.connect(self.host, self.userName, self.passwd, self.dbName, charset = self.charset)
        self.cur = self.con.cursor()

    def close(self):
        self.con.close()
        self.logfile.close()

    def executeUpdate(self, update):
        try:
            self.cur.execute(update)
            self.con.commit()
        except MySQLdb.Error, e:
            writeLog('insertUser2DB()', e)

    def executeQuery(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def insertUser2DB(self, user):
        insert = "INSERT INTO user_t(id, contributors_enabled, description, favourites_count, followers_count, "
        insert += "geo_enabled, lang, location, name, notifications, protected, screen_name, statuses_count, "
        insert += "time_zone, url, utc_offset, verified, created_at, friends_count) "
        insert += " VALUES(%(id)s, %(contributors_enabled)s, %(description)s, %(favourites_count)s, %(followers_count)s, "
        insert += "%(geo_enabled)s, %(lang)s, %(location)s, %(name)s, %(notifications)s, %(protected)s, %(screen_name)s, %(statuses_count)s, "
        insert += "%(time_zone)s, %(url)s, %(utc_offset)s, %(verified)s, %(created_at)s, %(friends_count)s)"
        try:
            self.cur.execute(insert, user)
            self.con.commit()
        except MySQLdb.Error, e:
            writeLog('insertUser2DB()', e)

    def insertTweet2DB(self, tweet):
        insert = "INSERT INTO status_t(id, favorited, in_reply_to_screen_name, in_reply_to_user_id, "
        insert += "in_reply_to_status_id, truncated, text, user_id, retweet_count, retweeted, "
        insert += "created_at, relative_created_at) "
        insert += "VALUES(%(id)s, %(favorited)s, %(in_reply_to_screen_name)s, %(in_reply_to_user_id)s, "
        insert += "%(in_reply_to_status_id)s, %(truncated)s, %(text)s, %(user_id)s, %(retweet_count)s, %(retweeted)s, "
        insert += "%(created_at)s, %(relative_created_at)s)"
        try:
            self.cur.execute(insert, tweet)
            self.con.commit()
            print "%s: %s" % (tweet['created_at'], tweet['text'])
        except MySQLdb.Error, e:
            self.writeLog('insertTweet2DB()', e)

    def getMonthlyData(self, date):
        query = "select text from status_t where DATE_FORMAT(created_at, '%%Y-%%m')=DATE_FORMAT('%s', '%%Y-%%m')" % date
        try:
            self.cur.execute(query)
        except MySQLdb.Error, e:
            self.writeLog('getMonthlyData()', e)
        numrow = int(self.cur.rowcount)
        for i in xrange(numrow):
            r = self.cur.fetchone()
            yield r

    def insertKeyword2DB(self, keyword, count, date):
        insert = "insert into monthlyAnalysis(keyword, count, date) value('%s', %s, '%s')" % (keyword, count, date)
        try:
            self.cur.execute(insert)
            self.con.commit()
        except MySQLdb.Error, e:
            self.writeLog('saveMonthlyData()', e)

    def getMonthlyKeywordCount(self, keyword, date):
        query = "SELECT count FROM monthlyAnalysis WHERE keyword like '%%%s%%' and DATE_FORMAT(date, '%%Y-%%m')=DATE_FORMAT('%s', '%%Y-%%m')" % (keyword, date)
        try:
            self.cur.execute(query)
        except MySQLdb.Error, e:
            self.writeLog('getMonthlyKeywordCount()', e)
        return self.cur.fetchall()

    def getCurrentTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def writeLog(self, funtionName, errorInfo):
        currentTime = self.getCurrentTime()
        err = "%s: %s Error %d: %s\n" % (currentTime, funtionName, errorInfo.args[0], errorInfo.args[1])
        self.logfile.write(err)

    def computeAndSaveMonthlyTweetCount(self, date):
        query = "SELECT COUNT(id) FROM status_t WHERE DATE_FORMAT(created_at, '%%Y-%%m')=DATE_FORMAT('%s', '%%Y-%%m')" %  date
        try:
            self.cur.execute(query)
        except MySQLdb.Error, e:
            self.writeLog('getMonthlyTweetCount()', e)
        rows = self.cur.fetchall()
        print rows
        select = "insert into monthlyAnalysis(keyword, date, count) VALUES('TWEET_COUNT', '%s', %d)"
        if rows == ():
            select = select % (date, 0)
        else:
            select = select % (date, rows[0][0])
        try:
            self.cur.execute(select)
            self.con.commit()
        except MySQLdb.Error, e:
            self.writeLog('getMonthlyTweetCount()', e)

    def getMonthlyTweetCount(self, date):
        query = "SELECT count FROM monthlyAnalysis WHERE keyword='TWEET_COUNT' and DATE_FORMAT(date, '%%Y-%%m')=DATE_FORMAT('%s', '%%Y-%%m')" % date
        try:
            self.cur.execute(query)
        except MySQLdb.Error, e:
            self.writeLog('getMonthlyTweetCount()', e)

        rows = self.cur.fetchall()
        if rows == ():
            return 0
        else:
            return rows[0][0]

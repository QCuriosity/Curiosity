import sys
sys.path.append("../database/")
from mysql import *
import twitter
import time
import MySQLdb
import os

reload(sys)
sys.setdefaultencoding('utf-8')

class collection_twitter:
    def __init__(self, isAuth = False,
                        consumer_key = "",
                        consumer_secret = "",
                        access_token_key = "",
                        access_token_secret = ""):
        """ isAuth == True, using authentication connect, isAuth == False, using public conncet"""
        self.isAuth = isAuth
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.logfile = open("../logs/collection_twitter.log", 'a')

        if isAuth == True:
            self.twitter_api = twitter.Api(self.consumer_key, self.consumer_secret,
                    self.access_token_key, self.access_token_secret)
        else:
            self.twitter_api = twitter.Api()

    def __del__(self):
        self.logfile.close()

    def writeLog(self, log):
        self.logfile.write(log)

    def conver_time_format(self, src_time):
        """ convert time format %a %b %d %H:%M:%S +0000 %Y to %Y-%m-%d %H:%M:%S """
        SRC_TIMEFORMAT = '%a %b %d %H:%M:%S +0000 %Y'
        RC_TIMEFORMAT = '%Y-%m-%d %H:%M:%S'
        rc_time = time.strftime(RC_TIMEFORMAT, time.strptime(src_time, SRC_TIMEFORMAT))
        return rc_time

    def find_user(self, db):
        """ random find a user add in db """
        query = "SELECT id from user_t"
        rows = db.executeQuery(query)

        #for r in rows:
        num = len(rows)
        i = 0;
        while(i < 600):
            i += 1
            idx = random.randint(0, num-1)
            r = rows[idx]
            user = {}
            try:
                users = self.twitter_api.GetFriends(r[0])
            except:
                print 'python-twitter error, sleep 10 min'
                time.sleep(600)
                continue
            for u in users:
                user['id'] = u.GetId()
                user['contributors_enabled'] = u.GetContributorsEnabled()
                user['description'] = u.GetDescription()
                user['favourites_count'] = u.GetFavouritesCount()
                user['followers_count'] = u.GetFollowersCount()
                user['geo_enabled'] = u.GetGeoEnabled()
                user['lang'] = u.GetLang()
                user['location'] = u.GetLocation()
                user['name'] = u.GetName()
                user['notifications'] = u.GetNotifications()
                user['protected'] = u.GetProtected()
                user['screen_name'] = u.GetScreenName()
                user['statuses_count'] = u.GetStatusesCount()
                user['time_zone'] = u.GetTimeZone()
                user['url'] = u.GetUrl()
                user['utc_offset'] = u.GetUtcOffset()
                user['verified'] = u.GetVerified()
                user['created_at'] = my.conver_time_format(u.GetCreatedAt())
                user['friends_count'] = u.GetFriendsCount()
                try:
                    db.insertUser2DB(user)
                except:
                    continue
                print user
            print idx
            time.sleep(120)

    def getCurrentTime(self):
        cctime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return cctime

    def retryGetTimeline(self, user_id, name):
        for i in range(3):
            try:
                print "%s: start get status for '%s'(%d)" % (self.getCurrentTime(), name, user_id)
                statuses = self.twitter_api.GetUserTimeline(id = user_id, count = 100)
                return statuses
            except:
                print 'python_twitter error, sleep 15 seconds'
                err = "collect_tweets: error user: %d\n" % (user_id)
                self.writeLog(err)
                time.sleep(15)
                continue
        return []

    def collect_tweets(self, db):
        """ collect tweets to DB """
        query = "SELECT id, name from user_t where processed is null or processed=false"
        rows = db.executeQuery(query)
        print "rows num: %d" % len(rows)
        for r in rows:
            statuses = self.retryGetTimeline(r[0], r[1])
            if len(statuses) > 0:
                print "%s: insert user status to DB. %d: %s" % (self.getCurrentTime(), r[0], r[1])
            else:
                continue
            for s in statuses:
                status = {}
                status['id'] = s.GetId()
                status['favorited'] = s.GetFavorited()
                status['in_reply_to_screen_name'] = s.GetInReplyToScreenName()
                status['in_reply_to_user_id'] = s.GetInReplyToUserId()
                status['in_reply_to_status_id'] = s.GetInReplyToStatusId()
                status['truncated'] = s.GetTruncated()
                status['text'] = s.GetText()
                status['user_id'] = s.GetUser().GetId()
                status['retweet_count'] = s.GetRetweetCount()
                status['retweeted'] = s.GetRetweeted()
                status['created_at'] = self.conver_time_format(s.GetCreatedAt())
                status['relative_created_at'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

                try:
                    db.insertTweet2DB(status)
                except:
                    print "insert error"
                    continue
                updateSQL = "update user_t set processed=true where id=%s" % r[0]
                db.executeUpdate(updateSQL);
            log = "%s: collect_tweets(): processed user: %d\n" % (self.getCurrentTime(), r[0])
            self.writeLog(log)
            print "wait next user..."
            time.sleep(15)

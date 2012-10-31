from iuser import OAuth_api
import MySQLdb
import time
import os

fp = open("miss_status_user.log", "a")

my = OAuth_api(True)
db = MySQLdb.connect('localhost', 'root', 'password', 'curiosity', charset = 'utf8')
cur = db.cursor()

query = "SELECT id from user_t"
cur.execute(query)
rows = cur.fetchall()

for r in rows:
    if r[0] < 526316060:
        continue
    try:
        statuses = my.api.GetUserTimeline(id = r[0], count = 200)
    except:
        print 'python_twitter error, sleep 10 min'
        err = "error user: %d\n" % (r[0])
        fp.write(err)
        time.sleep(180)
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
        status['created_at'] = my.conver_time_format(s.GetCreatedAt())
        status['relative_created_at'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        insert = "INSERT INTO status_t(id, favorited, in_reply_to_screen_name, in_reply_to_user_id, "
        insert += "in_reply_to_status_id, truncated, text, user_id, retweet_count, retweeted, "
        insert += "created_at, relative_created_at) "
        insert += "VALUES(%(id)s, %(favorited)s, %(in_reply_to_screen_name)s, %(in_reply_to_user_id)s, "
        insert += "%(in_reply_to_status_id)s, %(truncated)s, %(text)s, %(user_id)s, %(retweet_count)s, %(retweeted)s, "
        insert += "%(created_at)s, %(relative_created_at)s)"
        try:
            print status
            cur.execute(insert, status)
            db.commit()
        except MySQLdb.Error, e:
            err = "Error %d: %s\n\n" % (e.args[0], e.args[1])
            continue
    log = "processed user: %d\n" % (r[0])
    fp.write(log)
    time.sleep(15)
	
if db:
    db.close()
fp.close()

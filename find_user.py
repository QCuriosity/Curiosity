from iuser import OAuth_api
import MySQLdb
import time
import random
import os

fp = open("find_user.log", "a")

my = OAuth_api(True)
db = MySQLdb.connect('localhost', 'root', 'password', 'curiosity', charset = 'utf8')
cur = db.cursor()

query = "SELECT id from user_t"
cur.execute(query)
rows = cur.fetchall()

#for r in rows:
num = len(rows)
i = 0;
while(i < 600 ):
    i += 1
    idx = random.randint(0, num-1)
    r = rows[idx]
    user = {}
    try:
        users = my.api.GetFriends(r[0])
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
        insert = "INSERT INTO user_t(id, contributors_enabled, description, favourites_count, followers_count, "
        insert += "geo_enabled, lang, location, name, notifications, protected, screen_name, statuses_count, "
        insert += "time_zone, url, utc_offset, verified, created_at, friends_count) "
        insert += " VALUES(%(id)s, %(contributors_enabled)s, %(description)s, %(favourites_count)s, %(followers_count)s, "
        insert += "%(geo_enabled)s, %(lang)s, %(location)s, %(name)s, %(notifications)s, %(protected)s, %(screen_name)s, %(statuses_count)s, "
        insert += "%(time_zone)s, %(url)s, %(utc_offset)s, %(verified)s, %(created_at)s, %(friends_count)s)"
        try:
            print insert, user
            cur.execute(insert, user)
            db.commit()
        except MySQLdb.Error, e:
            err = "Error %d: %s\n\n" % (e.args[0], e.args[1])
            print err
            fp.write(err)
            continue
        print user
    print idx
    time.sleep(120)
if db:
    db.close()
fp.close()

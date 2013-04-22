from iuser import OAuth_api
import MySQLdb
import time
import random
import os

fp = open("miss_user.log", "a")

host = ""
username = ""
password = ""
dbname = ""

my = OAuth_api(True)
db = MySQLdb.connect(host, username, password, dbname, charset = 'utf8')
cur = db.cursor()

query = "SELECT id from user_t WHERE geo_enabled is null"
cur.execute(query)
rows = cur.fetchall()

for r in rows:
    id = r[0]
    try:
        u = my.api.GetUser(id)
    except:
        print 'python-twitter error, sleep 10 min'
        miss_user = "%d\n" % id
        fp.write(miss_user)
        time.sleep(600)
        continue
    user = {}
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
#try:
    user['created_at'] = my.conver_time_format(u.GetCreatedAt())
#except:
#continue
    user['friends_count'] = u.GetFriendsCount()
    update = "UPDATE user_t SET contributors_enabled = %(contributors_enabled)s, description = %(description)s, "
    update += "favourites_count = %(favourites_count)s, followers_count = %(followers_count)s, geo_enabled = %(geo_enabled)s, "
    update += "lang = %(lang)s, location = %(location)s, name = %(name)s, notifications = %(notifications)s, "
    update += "protected = %(protected)s, screen_name = %(screen_name)s, statuses_count = %(statuses_count)s, "
    update += "time_zone = %(time_zone)s, url = %(url)s, utc_offset = %(utc_offset)s, verified = %(verified)s, "
    update += "created_at = %(created_at)s, friends_count = %(friends_count)s WHERE id = %(id)s"
    try:
        print user
        cur.execute(update, user)
        db.commit()
    except MySQLdb.Error, e:
            err = "Error %d: %s\n\n" % (e.args[0], e.args[1])
            print err
            continue
    time.sleep(30)

if db:
    db.close()

fp.close()

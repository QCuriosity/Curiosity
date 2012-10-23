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
        user['name'] = u.GetName()
        user['screen_name'] = u.GetScreenName()
        user['description'] = u.GetDescription()
        user['created_at'] = my.conver_time_format(u.GetCreatedAt())
        insert = "INSERT INTO user_t(id, name, screen_name, description, created_at) "
        insert += " VALUES(%(id)s, %(name)s, %(screen_name)s, %(description)s, %(created_at)s)"
        try:
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

from iuser import OAuth_api
import MySQLdb
import time

my = OAuth_api
db = MySQLdb.connect('localhost', 'root', 'password', 'curiosity', charset = 'utf8')
cur = db.cursor()

followers = api.GetFriends()
query = "SELECT id from user_t"
insert = "INSERT INTO user_t(id, name, screen_name, description, created_at) "
cur.execute(query)
rows = cur.fetchall()

for r in rows:
    user = {}
    users = my.api.GetFriends(r[0])
    for u in users:
        user['id'] = u.GetId()
        user['name'] = u.GetName()
        user['screen_name'] = u.GetScreenName()
        user['description'] = u.GetDescription()
        user['created_at'] = my.conver_time_format(u.GetCreatedAt())
        insert += " VALUES(%(id)s, %(name)s, %(screen_name)s, %(description)s, %(created_at)s)"
        print user
        try:
            cur.execute(insert, user)
            con.commit()
        except:
            continue

if db:
    db.close()

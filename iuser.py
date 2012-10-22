import twitter
import time
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

class OAuth_api:
    api = None    
    isAuth = False
    consumer_key = "BhQeZKp63OxBSu7KAUtug"
    consumer_secret = "aVqwJOrK4wrVVxau0UBk4rwzdwLkPGLY3BAP3H2V7Dw";
    access_token_key = "830501012-Z8iYaTMrX3wjY5q0o5a0NAIfSBQF2Ywmk9NZ0Ksd";
    access_token_secret = "e8mP0eHyB6wH19HVBk8Dp2dr14DHF0K9bZxYCRA8";
    def __init__(self, isAuth):
        """isAuth == True, using authentication connect, isAuth == False, using public conncet"""
        self.isAuth = isAuth
        if isAuth == True
            self.api = twitter.Api(self.consumer_key, self.consumer_secret,
                    self.access_token_key, self.access_token_secret)
        else
            self.api = twitter.Api()

    def create_many_friendship(self, users):
        for s in users:
            self.api.CreateFriendship(s.GetId())
            print "\tfriendship successed:", s.name

    def get_friends(self):
        friends = self.api.GetFriends()
        for s in friends:
            all_friends = []
            all_friends = self.api.GetFriends(s.GetId())
            print "my friends:", s.name, "\ncount:", len(all_friends)
            self.create_many_friendship(users=all_friends)
        
        print "\n all friends count:", len(all_friends)
            
    def get_ifriends(self):
        all_fos = self.api.GetFriends()
        for f in all_fos:
            print j, ":", f.name
            j += 1
        return all_fos

    def conver_time_format(self, src_time):
        SRC_TIMEFORMAT = '%a %b %d %H:%M:%S +0000 %Y'
        RC_TIMEFORMAT = '%Y-%m-%d %H:%M:%S'
        print src_time
        rc_time = time.strftime(RC_TIMEFORMAT, time.strptime(src_time, SRC_TIMEFORMAT))
        return rc_time

    def friends2db(self, user):
        db = MySQLdb.connect('localhost', 'root', 'password', 'curiosity', charset = 'utf8')
        cur = db.cursor()
        user['created_at'] = self.conver_time_format(user['created_at'])
        insert = "INSERT INTO user_t(id, contributors_enabled, create_at, description,\
favourites_count, followers_count, geo_enabled, lang, location, name,\
notifications, protected, screen_name, statuses_count, time_zone, url,\
utc_offset, verified) VALUES(%(id)s, %(contributors_enabled)s,\
%(create_at)s, %(description)s,%(favourites_count)s, %(followers_count)s,\
%(geo_enabled)s, %(lang)s, %(location)s, %(name)s,%(no)s, \
%(protected)s, %(screen_name)s, %(statuses_count)s, %(time_zone)s, %(url)s,\
%(utc_offset)s, %(verified)s)"
        print insert
        cur.execute(insert, user)
        db.commit()
        if db:
            db.close()

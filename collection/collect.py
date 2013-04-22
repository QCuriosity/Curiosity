import sys
sys.path.append("../database/")
from mysql import *
from collection_twitter import *

db = mysql(host, user, passwd, dbName)
db.connect()

collection = collection_twitter(True)

collection.collect_tweets(db)

b.close()

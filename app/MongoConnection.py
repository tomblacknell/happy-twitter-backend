from pymongo import MongoClient
import urllib
from bson.son import SON


class MongoConnection(object):
    def __init__(self):
        username = urllib.parse.quote_plus('blackers')
        password = urllib.parse.quote_plus('a2J4!?Bbc4120')
        client = MongoClient('mongodb://%s:%s@vm9.blacknell.co.uk' % (username, password))
        self.db = client.tweets
        self.db.authenticate('tweetuser','soMawRK2J6qyBH8')

    def get_collection(self, name):
        self.collection = self.db[name]


class TweetCollection(MongoConnection):
    def __init__(self):
        super(TweetCollection, self).__init__()
        self.get_collection('tweets_live')

    def get_num_of_tweets(self):
        result = self.collection.find({}).count()
        if result:
            return result
        else:
            return 420

    def get_tweets_today_by_location(self):
        pipeline = [
            {"$group": {"_id": "$location", "number": {"$sum": 1}}},
            {"$sort": SON([("number", -1)])}
        ]
        result = self.collection.aggregate(pipeline)
        if result:
            return result
        else:
            return 420

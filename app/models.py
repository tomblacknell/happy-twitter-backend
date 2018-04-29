
import pymongo
from pymongo import MongoClient
import urllib
from bson.son import SON
import datetime
from bson import json_util
import json

# Models

# Authored by Tom Blacknell

# Collection models are instances of MongoConnection, a class that connects and authenticates with the database.
# Collection models have methods for requesting queries and metrics from the database
# Queries are fulfilled, and the results returned upstream


class MongoConnection(object):
    def __init__(self):
        username = urllib.parse.quote_plus('blackers')
        password = urllib.parse.quote_plus('a2J4!?Bbc4120')
        client = MongoClient('mongodb://%s:%s@vm9.blacknell.co.uk' % (username, password))
        self.db = client.tweets
        self.db.authenticate('tweetuser', 'soMawRK2J6qyBH8')

    def get_collection(self, name):
        self.collection = self.db[name]


class TopicCollection(MongoConnection):
    def __init__(self):
        super(TopicCollection, self).__init__()
        self.get_collection('topics')

    def get_topic_explore(self, week_view):

        num_days = "week"
        if week_view == "0":
            num_days = "month"

        result = self.collection.find({'_id': num_days})
        if result:
            return json_util.dumps(result)
        else:
            return 420


class TopicSmallCollection(MongoConnection):
    def __init__(self):
        super(TopicSmallCollection, self).__init__()
        self.get_collection('topics_small')

    def get_topics(self, week_view):

        num_days = "week"
        if week_view == "0":
            num_days = "month"

        result = self.collection.find({'_id': num_days})
        if result:
            return json_util.dumps(result)
        else:
            return 420


class TweetCollection(MongoConnection):
    def __init__(self):
        super(TweetCollection, self).__init__()
        self.get_collection('tweets_2')

    def get_region_stats(self, region_name, week_view):

        num_days = 7
        id = "week"
        if week_view == "0":
            num_days = 30
            id = "month"

        tweets = self.collection.find({
            "created_at": {
                "$lt": datetime.datetime.now(),
                "$gte": datetime.datetime.now() - datetime.timedelta(days=num_days)
            },
            "location": region_name
        })

        num_tweets = tweets.count()

        topics = self.db['topics_small'].find_one({"_id": id})["data"]

        topic_counts = {}
        topic_terms = []
        for topic in json.loads(topics):
            terms = []
            for term in topic["terms"]:
                terms.append(term["term"])
            topic_terms.append({"topic":topic["topic"], "terms":terms})
            topic_counts[topic["topic"]] = 0

        for tweet in tweets:
            for topic_term in topic_terms:
                for term in topic_term["terms"]:
                    if term in tweet["text"].lower():
                        topic_counts[topic_term["topic"]] = topic_counts.get(topic_term["topic"]) + 1

        final_topic_counts = []
        for topic in topic_counts.keys():
            final_topic_counts.append({"topic":topic, "count":topic_counts[topic]})

        print("Final topic counts:")
        print(final_topic_counts)

        result = {"name": region_name, "count": num_tweets, "topics": final_topic_counts}

        if result:
            return result
        else:
            return 420

    def get_num_of_tweets(self, week_view):

        num_days = 7

        if week_view == "0":
            num_days = 30

        aggregator = [
            {
                "$match": {
                    "created_at": {
                        "$lt": datetime.datetime.now(),
                        "$gte": datetime.datetime.now() - datetime.timedelta(days=num_days)
                    }
                }
            },
            {
                "$count": "count"
            }
        ]

        result = self.collection.aggregate(aggregator)

        if result:
            return json_util.dumps(result)
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

    def get_latest_tweets(self):
        result = self.collection.find().sort("created_at", pymongo.DESCENDING).limit(5)
        if result:
            return json_util.dumps(result)
        else:
            return 420

    def get_tweet_locations(self, week_view):

        num_days = 7

        if week_view == "0":
            num_days = 30


        result = self.collection.aggregate([
            {
                "$match": {
                    "created_at": {
                        "$lt": datetime.datetime.now(),
                        "$gte": datetime.datetime.now() - datetime.timedelta(days=num_days)
                    }
                }
            },
            {
                "$project": {
                    "created_at": 0,
                    "_id": 0,
                    "text": 0,
                    "location": 0
                }
            }
        ])

        if result:
            return json_util.dumps(result)
        else:
            return 420

    def get_tweet_rate(self, weekView):

        num_days = 7
        interval = 30

        if weekView == "0":
            num_days = 30
            interval = 60

        result = self.collection.aggregate([
            {
                "$match": {
                    "created_at": {
                        "$lt": datetime.datetime.now(),
                        "$gte": datetime.datetime.now() - datetime.timedelta(days=num_days)
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "hour": {"$hour": "$created_at"},
                        "dayOfYear": {"$dayOfYear": "$created_at"},
                        "interval": {
                            "$subtract": [
                                {"$minute": "$created_at"},
                                {"$mod": [{"$minute": "$created_at"}, interval]}
                            ]
                        }
                    },
                    "count": {"$sum": 1}
                }
            }
        ])

        if result:
            return json_util.dumps(result)
        else:
            return 420

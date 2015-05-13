__author__ = 'gsvic'

from pymongo import MongoClient
from datetime import datetime, timedelta
import time
import re

class Mongo():

    def __init__(self):
        client = MongoClient()
        self.db = client.flutrack

    def GetData(self):
        return self.db.tweets

    def checkAggravation(self, tweet):
        tweet_date = datetime.fromtimestamp(float(tweet['timestamp_ms']/1000))
        aggravation_limit = tweet_date - timedelta(days=8)

        aggravation_limit = time.mktime(aggravation_limit.timetuple())*1000
        user_id = tweet['user_id']
        data = self.db.tweets.find({'$and':[{'user_id': user_id},
                                            {'timestamp_ms': {'$gt': aggravation_limit}}]
                                    })

        aggravation_pattern = "getting worse|get worse|weaker|deterioration|deteriorate|worsening|" \
                              "degenerate|regress|exacerbate|relapse|intensify|compound|" \
                              "Become aggravated|get into a decline|go to pot"
        if data.count() > 0:
            try:
                re.search(aggravation_pattern, tweet['text']).group()
                return True
            except:
                pass

        return False
__author__ = 'gsvic'

import tweepy
import json
from pymongo import MongoClient


class FluTrackStreamer:
    def __init__(self):
        pass

    class FluListener(tweepy.StreamListener):
            #MongoDB Client
            client = MongoClient('mongodb://localhost:27017')
            db = client.flutrack.tweets

            def on_data(self, raw_data):
                doc = (json.loads(raw_data))
                self.db.insert(doc)
                return True
            def on_error(self, status_code):
                print (status_code)
                return False

    def StreamData(self):
        #OAuth
        key = ""
        secret = ""
        access_token = ""
        access_secret = ""

        listener = self.FluListener()
        auth = tweepy.OAuthHandler(key, secret)
        auth.set_access_token(access_token, access_secret)

        print ("Start streaming...")
        stream = tweepy.Stream(auth=auth, listener=listener)
        keywords = ['flu', 'chills', 'sore', 'throat',
                                    'headache', 'runny', 'nose', 'vomiting',
                                    'sneazing', 'fever', 'diarrhea', 'dry', 'cough']

        data = stream.filter(track=keywords)


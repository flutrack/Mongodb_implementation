__author__ = 'gsvic'

import tweepy
import json
from pymongo import MongoClient
from DataStore import Mongo


class FluTrackStreamer:
    def __init__(self):
        pass

    class FluListener(tweepy.StreamListener):
            #MongoDB Client
            client = MongoClient()
            tweets = client.flutrack.tweets
            users = client.flutrack.twitter_data
            whole_tweets = client.flutrack.whole_tweets

            def on_data(self, raw_data):
                doc = (json.loads(raw_data))
                print "Check..."

                doc['timestamp_ms'] = int(doc['timestamp_ms'])
                self.whole_tweets.insert(doc)

                #Creating the tweet record
                user_id = doc['user']['screen_name']
                doc['user'].pop('screen_name', None)
                doc['user_id'] = user_id
                user_details = doc['user']
                doc['aggravation'] = Mongo().checkAggravation(doc)
                doc.pop('user', None)

                #Creating the user record
                user = dict()
                user['_id'] = user_id
                user['user'] = user_details
                self.users.update({'_id': user_id}, user, True)
                self.tweets.insert(doc)

                print "OK"


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

        data = stream.filter(track=keywords, )


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
import pymongo
from datetime import datetime, timedelta
import time

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def tweets(request):
    if request.method == 'GET':
        search_param = request.GET.get('s', '')
        limit_param = int(request.GET.get('limit', 20))
        time_param = int(request.GET.get('time', 0))

        time_limit_ms = datetime.now() #- timedelta(days=time_param)
        print "DATELIM: ", time_limit_ms
        time_limit_ms = time.mktime(time_limit_ms.timetuple())

        search_query = search_param.split("OR")
        search_query = ' '.join(search_query)
        search_query = search_param.split("AND")
        search_query = ' '.join(search_query)
	
	print "Search QUERY: ",search_query
        #Connect to MongoDB
        client = pymongo.MongoClient()
        db = client.flutrack
        data = db.tweets

        if search_param:
            data = [CleanTweet(d) for d in data.find({"$text": {"$search": search_query}}
            ).sort('timestamp_ms', pymongo.DESCENDING) if d['geo']]
        else:
            data = [CleanTweet(d) for d in data.find().sort('timestamp_ms', pymongo.DESCENDING)
                    if d['geo']]

        data_count = len(data)
        if limit_param < data_count and limit_param >= 0:
            data = data[0:limit_param]

    return JSONResponse(data)

def CleanTweet(tweet):
                cleaned = dict()
                cleaned['user_name'] = tweet['user_id']
                cleaned['tweet_text'] = tweet['text']
                cleaned['tweet_date'] = datetime.fromtimestamp(tweet['timestamp_ms']/1000)
                cleaned['aggravation'] = "0"
                try:
                    geo = tweet['geo']['coordinates']
                    cleaned['longitude'] = str(geo[0])
                    cleaned['latitude'] = str(geo[1])
                except:
                    cleaned['longitude'] = ''
                    cleaned['latitude'] = ''

                return cleaned

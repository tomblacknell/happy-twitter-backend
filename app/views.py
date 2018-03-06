
# Create your views here.

from django.http import HttpResponse, JsonResponse
from .MongoConnection import TweetCollection


def total_tweets(request):
    if request.method == 'GET':

        tweets = TweetCollection()
        num = tweets.get_num_of_tweets()

        return JsonResponse({'total_tweets':num}, safe=False, status=200)
    else:
        return HttpResponse(status=400)


def get_tweets_today_by_location(request):
    if request.method == 'GET':

        tweets = TweetCollection()
        result = tweets.get_tweets_today_by_location()

        return JsonResponse([doc for doc in result], safe=False, status=200)
    else:
        return HttpResponse(status=400)
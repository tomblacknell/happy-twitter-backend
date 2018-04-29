
from django.http import HttpResponse, JsonResponse
from .models import TweetCollection
from .models import TopicCollection
from .models import TopicSmallCollection
from app import region_names

# Views

# Authored by Tom Blacknell

# Views handle checking the request type and validating parameters
# Request is then fulfilled by the model (models.py), and returned in the JsonResponse


# Region Stats Endpoint
def region_stats(request, region_name, week_view):

    if request.method == 'GET':
        if week_view == "0" or week_view == "1":
            if region_name in region_names.region_names:
                tweets = TweetCollection()
                result = tweets.get_region_stats(region_name, week_view)
                return JsonResponse(result, safe=False, status=200)

    return HttpResponse(status=400)


# Topics Endpoint
def topics(request, weekView):

    if request.method == 'GET':
        if weekView == "0" or weekView == "1":
            topics_small = TopicSmallCollection()
            topics = topics_small.get_topics(weekView)
            return JsonResponse(topics, safe=False, status=200)

    return HttpResponse(status=400)


# Advanced Topic Explore Endpoint
def topic_explore(request, weekView):

    if request.method == 'GET':
        if weekView == "0" or weekView == "1":
            topics = TopicCollection()
            topic_explore = topics.get_topic_explore(weekView)
            return JsonResponse(topic_explore, safe=False, status=200)

    return HttpResponse(status=400)


# Total Tweets Endpoint
def total_tweets(request, weekView):

    if request.method == 'GET':
        if weekView == "0" or weekView == "1":
            tweets = TweetCollection()
            num = tweets.get_num_of_tweets(weekView)
            return JsonResponse(num, safe=False, status=200)

    return HttpResponse(status=400)


# Tweet Rate Endpoint
def tweet_rate(request, weekView):

    if request.method == 'GET':
        if weekView == "0" or weekView == "1":
            tweets = TweetCollection()
            result = tweets.get_tweet_rate(weekView)
            return JsonResponse(result, safe=False, status=200)

    return HttpResponse(status=400)


# Latest Tweets Endpoint
def latest_tweets(request):

    if request.method == 'GET':
        tweets = TweetCollection()
        result = tweets.get_latest_tweets()
        return JsonResponse(result, safe=False, status=200)
    else:
        return HttpResponse(status=400)


# Tweet Locations Endpoint
def tweet_locations(request, weekView):

    if request.method == 'GET':
        if weekView == "0" or weekView == "1":
            tweets = TweetCollection()
            result = tweets.get_tweet_locations(weekView)
            return JsonResponse(result, safe=False, status=200)

    return HttpResponse(status=400)
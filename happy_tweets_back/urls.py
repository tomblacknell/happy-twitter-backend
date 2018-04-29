
from django.conf.urls import url
from app import views

# URLs

# Authored by Tom Blacknell

# Endpoint URLs are defined using regular expressions
# Matched URLs sent to the relevant view

# URL Patterns
urlpatterns = [
    url(r'^api/total-tweets/(?P<weekView>[0-1])/$', views.total_tweets),
    url(r'^api/tweet-rate/(?P<weekView>[0-1])/$', views.tweet_rate),
    url(r'^api/latest-tweets/$', views.latest_tweets),
    url(r'^api/tweet-locations/(?P<weekView>[0-1])$', views.tweet_locations),
    url(r'^api/topic-explore/(?P<weekView>[0-1])$', views.topic_explore),
    url(r'^api/topics/(?P<weekView>[0-1])$', views.topics),
    url(r'^api/region-stats/(?P<region_name>[A-Za-z\s]*)/(?P<week_view>[0-1])$', views.region_stats)
]

from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^api/total-tweets/$', views.total_tweets),
    url(r'^api/tweets-today/$', views.get_tweets_today_by_location)
]
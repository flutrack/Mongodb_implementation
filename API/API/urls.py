from django.conf.urls import include, url
from django.contrib import admin
from tweets import views

urlpatterns = [
    url(r'^FlutrackAPI/$', views.tweets),
]

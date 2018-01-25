from django.conf.urls import url

from . import views

urlpatterns = [
    # Capture any characters until reaching a forward slash & pass to views.index as 'subreddit' param.
    # If any characters appear after the forward slash, will fail to match.
    url(r'^(?P<subreddit>[^/]+)/$', views.index, name='index')
]

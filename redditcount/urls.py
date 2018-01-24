from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<subreddit>[\w]+)', views.index, name='index')
]

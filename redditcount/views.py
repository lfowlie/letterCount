# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse


def index(request, subreddit):
    return HttpResponse("Parsing {}.".format(subreddit))
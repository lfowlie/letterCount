# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from praw.exceptions import APIException
from prawcore import PrawcoreException, Redirect, NotFound

from redditcount import redditcount_manager

LETTER_TO_COUNT = "p"


def index(request, subreddit):
    try:
        letter_count, submission_count = redditcount_manager.get_count_and_update(subreddit, LETTER_TO_COUNT)
    except (Redirect, NotFound):
        # Reddit API redirects to '/subreddits/search' for unknown subreddits, and returns 404 for invalid subreddit
        # names (i.e. too long or invalid character)
        return HttpResponse('Error requesting subreddit, subreddit name may be incorrect.', status=404)
    except (APIException, PrawcoreException):
        return HttpResponse('An error occurred while requesting subreddit submissions.', status=500)

    return HttpResponse("The letter '{}' occurs {} times in the most recent {} posts on /r/{}.".format(
        LETTER_TO_COUNT, letter_count, submission_count, subreddit))

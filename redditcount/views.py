# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from praw.exceptions import APIException
from prawcore import PrawcoreException, Redirect, NotFound

from redditcount.reddit_client import RedditClient


def index(request, subreddit):
    count = 0
    try:
        submissions = RedditClient().get_new_submissions_for_subreddit(subreddit)
        for submission in submissions:
            title = submission.title
            if title:
                count += title.lower().count('p')
    except (Redirect, NotFound):
        # Reddit API redirects to '/subreddits/search' for unknown subreddits, and returns 404 for invalid subreddit
        # names (i.e. too long or invalid character)
        return HttpResponse('Error requesting subreddit, subreddit name may be incorrect.')

    except (APIException, PrawcoreException) as requestError:
        return HttpResponse('Error requesting subreddit submissions: {}.'.format(requestError))

    return HttpResponse("The letter 'p' occurs {} times in /r/{}.".format(count, subreddit))

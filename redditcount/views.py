# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from praw.exceptions import APIException
from prawcore import PrawcoreException, Redirect, NotFound

import letter_count_util
from redditcount.reddit_client import RedditClient


def index(request, subreddit):
    titles = []
    try:
        submissions = RedditClient().get_new_submissions_for_subreddit(subreddit)
        for submission in submissions:
            title = submission.title
            if title:
                titles.append(title.lower())
    except (Redirect, NotFound):
        # Reddit API redirects to '/subreddits/search' for unknown subreddits, and returns 404 for invalid subreddit
        # names (i.e. too long or invalid character)
        return HttpResponse('Error requesting subreddit, subreddit name may be incorrect.')

    except (APIException, PrawcoreException) as requestError:
        return HttpResponse('Error requesting subreddit submissions: {}.'.format(requestError))

    count = letter_count_util.calculate_substring_count_in_string_list("p", titles)
    return HttpResponse("The letter 'p' occurs {} times in the most recent 1000 posts on /r/{}.".format(count, subreddit))

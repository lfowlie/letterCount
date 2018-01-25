import praw


class RedditClient(object):
    """
    Client for the Reddit API. Uses PRAW (Python Reddit API Wrapper) to handle authentication and requests.
    Note that Reddit rate limits to 60 requests per minute and only exposes the past 1000 submissions per subreddit.
    """

    def __init__(self):
        # In a real application these credentials should be in a database or file not checked into git.
        self._reddit = praw.Reddit(client_id='A25070mAGZwTTQ',
                                   client_secret='kXhGF2VHgpZkPnZMCFw3J2pjjt8',
                                   user_agent='python:com.mymo.lettercount:v1.0 (by /u/lfowlie)')

    def get_new_submissions_for_subreddit(self, subreddit):
        """
        Returns a ListingGenerator that can be iterated over for details of each submission. Limited to 1000 submissions.
        :param str subreddit: subreddit to query for submissions
        :rtype praw.models.ListingGenerator
        """
        return self._reddit.subreddit(subreddit).new(limit=1000)

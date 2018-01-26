import praw


class RedditClient(object):
    """
    Client for the Reddit API. Uses PRAW (Python Reddit API Wrapper) to handle authentication and requests.
    Note that Reddit rate limits to 60 requests per minute and only exposes the past 1000 submissions per subreddit.
    """

    def __init__(self, client_id, client_secret, user_agent):
        self._reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    def get_new_submissions_for_subreddit(self, subreddit):
        """
        Returns a ListingGenerator that can be iterated over for details of each submission. Limited to 1000 submissions.
        :param str subreddit: subreddit to query for submissions
        :rtype praw.models.ListingGenerator
        """
        return self._reddit.subreddit(subreddit).new(limit=1000)

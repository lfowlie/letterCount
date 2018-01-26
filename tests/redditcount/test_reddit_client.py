from mock import patch
from unittest import TestCase

from redditcount.reddit_client import RedditClient


class TestRedditClient(TestCase):
    @patch('praw.Reddit')
    def test_init(self, praw_reddit_mock):
        client_id = 'my_client_id'
        client_secret = 'my_client_secret'
        user_agent = 'my_user_agent'
        RedditClient(client_id, client_secret, user_agent)

        praw_reddit_mock.assert_called_once_with(client_id=client_id,
                                                 client_secret=client_secret,
                                                 user_agent=user_agent)

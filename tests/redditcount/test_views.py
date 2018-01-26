from datetime import timedelta
from django.test import Client
from django.utils import timezone
from mock import patch
from django.test import TestCase

from prawcore import NotFound, Redirect, PrawcoreException

from redditcount.models import SubredditLetterCount


class MockSubmission(object):
    def __init__(self, title):
        self.title = title


class MockResponse(object):
    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.headers = headers


class TestViews(TestCase):
    @patch('redditcount.views.redditcount_manager.RedditClient.get_new_submissions_for_subreddit')
    def test_index(self, mock_reddit_submissions):
        test_start = timezone.now()
        subreddit = 'some_subreddit'
        expected_letter_count = 4
        expected_submission_count = 3

        mock_reddit_submissions.return_value = [MockSubmission('puppy'), MockSubmission('How do I post?'),
                                                MockSubmission('Cake day')]
        client = Client()
        response = client.get('/reddit/{}/'.format(subreddit))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         "The letter 'p' occurs {} times in the most recent {} posts on /r/{}.".format(
                             expected_letter_count, expected_submission_count, subreddit))

        subreddit_letter_counts = SubredditLetterCount.objects.all()
        self.assertEqual(len(subreddit_letter_counts), 1)
        self.assertEqual(subreddit_letter_counts[0].name, subreddit)
        self.assertEqual(subreddit_letter_counts[0].letter, 'p')
        self.assertEqual(subreddit_letter_counts[0].letter_count, expected_letter_count)
        self.assertEqual(subreddit_letter_counts[0].submission_count, expected_submission_count)
        self.assertAlmostEqual(subreddit_letter_counts[0].count_updated, test_start, delta=timedelta(seconds=5))

    def test_index_with_persisted_count(self):
        test_start = timezone.now()
        subreddit = 'some_subreddit'
        expected_letter_count = 100
        expected_submission_count = 200

        persisted_count = SubredditLetterCount(name=subreddit, letter='p', letter_count=expected_letter_count,
                                               submission_count=expected_submission_count, count_updated=test_start)
        persisted_count.save()

        client = Client()
        response = client.get('/reddit/{}/'.format(subreddit))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         "The letter 'p' occurs {} times in the most recent {} posts on /r/{}.".format(
                             expected_letter_count, expected_submission_count, subreddit))

    @patch('redditcount.views.redditcount_manager.RedditClient.get_new_submissions_for_subreddit')
    def test_index_not_found_exception(self, mock_reddit_submissions):
        mock_reddit_submissions.side_effect = NotFound(MockResponse(status_code=404))

        client = Client()
        response = client.get('/reddit/some_subreddit/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, 'Error requesting subreddit, subreddit name may be incorrect.')

    @patch('redditcount.views.redditcount_manager.RedditClient.get_new_submissions_for_subreddit')
    def test_index_redirect_exception(self, mock_reddit_submissions):
        mock_reddit_submissions.side_effect = Redirect(MockResponse(status_code=301,
                                                                    headers={'location': '/subreddits/search'}))

        client = Client()
        response = client.get('/reddit/some_subreddit/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, 'Error requesting subreddit, subreddit name may be incorrect.')

    @patch('redditcount.views.redditcount_manager.RedditClient.get_new_submissions_for_subreddit')
    def test_index_praw_exception(self, mock_reddit_submissions):
        mock_reddit_submissions.side_effect = PrawcoreException(MockResponse(status_code=500))

        client = Client()
        response = client.get('/reddit/some_subreddit/')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content, 'An error occurred while requesting subreddit submissions.')

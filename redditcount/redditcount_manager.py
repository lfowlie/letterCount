from django.db import Error as dbError
from django.utils import timezone

import lettercount_util
from redditcount.models import SubredditLetterCount
from redditcount.reddit_client import RedditClient

SUBREDDIT_LETTER_COUNT_EXPIRATION_SECONDS = 900  # 15 minutes


def get_count_and_update(subreddit, letter_to_count):
    subreddit_letter_count = None
    try:
        subreddit_letter_count = SubredditLetterCount.objects.get(name=subreddit, letter=letter_to_count)
    except SubredditLetterCount.DoesNotExist:
        pass

    # if we have a persisted letter count that is less than 15 minutes old, just use that. Otherwise fetch from API
    if subreddit_letter_count and subreddit_letter_count.was_updated_within(SUBREDDIT_LETTER_COUNT_EXPIRATION_SECONDS):
        letter_count = subreddit_letter_count.letter_count
        submission_count = subreddit_letter_count.submission_count
    else:
        letter_count, submission_count = _request_count_from_api(subreddit, letter_to_count)

        try:
            _persist_count(subreddit_letter_count, letter_count, submission_count, subreddit, letter_to_count)
        except dbError:
            # swallow all database exceptions since we are currently only using SubredditLetterCount
            # to reduce request time. It would be wise to report these errors to the dev team in a real application.
            pass

    return letter_count, submission_count


def _request_count_from_api(subreddit, letter_to_count):
    titles = []
    submission_count = 0

    # In a real application these credentials should be in a database or file not checked into git.
    submissions = RedditClient(
        'A25070mAGZwTTQ',
        'kXhGF2VHgpZkPnZMCFw3J2pjjt8',
        'python:com.mymo.lettercount:v1.0 (by /u/lfowlie)'
    ).get_new_submissions_for_subreddit(subreddit)

    for submission in submissions:
        title = submission.title
        if title:
            titles.append(title.lower())
        submission_count += 1

    letter_count = lettercount_util.calculate_substring_count_in_string_list(letter_to_count, titles)
    return letter_count, submission_count


def _persist_count(subreddit_letter_count, letter_count, submission_count, subreddit, letter_to_count):
    now = timezone.now()

    if subreddit_letter_count:
        subreddit_letter_count.letter_count = letter_count
        subreddit_letter_count.submission_count = submission_count
        subreddit_letter_count.count_updated = now
    else:
        subreddit_letter_count = SubredditLetterCount(
            name=subreddit,
            letter=letter_to_count,
            letter_count=letter_count,
            submission_count=submission_count,
            count_updated=now
        )

    subreddit_letter_count.save()

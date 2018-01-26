# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone


class SubredditLetterCount(models.Model):
    name = models.CharField(max_length=200)
    letter = models.CharField(max_length=1)
    letter_count = models.IntegerField()
    submission_count = models.IntegerField()
    count_updated = models.DateTimeField()

    def was_updated_within(self, num_seconds):
        """
        True if this model's counts were updated in the last num_seconds seconds. False otherwise.
        :param int num_seconds: Number of seconds to check against count_updated
        :rtype bool
        """
        return datetime.timedelta(seconds=num_seconds) >= timezone.now() - self.count_updated

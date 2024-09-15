"""Contain the models for the polls app."""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """The Question model use as poll's question in the application."""

    question_text = models.CharField(max_length=200)
    published_date = models.DateTimeField('date published',
                                          default=timezone.now)
    end_date = models.DateTimeField('end date', blank=True, null=True)

    def was_published_recently(self):
        """Return False if the question was published more than 1 day ago."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now

    @admin.display(
        boolean=True,
        description="Published yet?",
    )
    def is_published(self):
        """Return True if current time has passed published_date."""
        return timezone.now() - self.published_date >= datetime.timedelta(0)

    @admin.display(
        boolean=True,
        description="Can vote?",
    )
    def can_vote(self):
        """
        Return True if the current time is between published_date and end_date.

        If end_date is None,
        voting is open indefinitely after the published date.
        """
        now = timezone.now()
        if self.end_date:
            return self.published_date <= now <= self.end_date
        return self.published_date <= now

    def __str__(self):
        """Easy-to-read in shell."""
        return self.question_text


class Choice(models.Model):
    """
    The Choice model used in polls application.

    Each choice associate with its question.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """Return the votes count for this choice."""
        return self.vote_set.count()

    def __str__(self):
        """Easy-to-read in shell."""
        return self.choice_text


class Vote(models.Model):
    """A vote by a user for a choice in a poll."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def question(self):
        """Return question associated with choice voted."""
        return self.choice.question

    def __str__(self):
        """Easy-to-read in shell."""
        return f"{self.user.username} vote for " \
               f"{self.choice.choice_text}"

"""Contain the models for the polls app."""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class Question(models.Model):
    """The Question model use as poll's question in the application."""

    question_text = models.CharField(max_length=200)
    published_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('end date', blank=True, null=True)

    def was_published_recently(self):
        """Return False if the question was published more than 1 day ago."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now

    def is_published(self):
        """Return True if current time has passed published_date."""
        return timezone.now() - self.published_date >= datetime.timedelta(0)

    def can_vote(self):
        """Return True if current time is between published_date and end_date."""
        if not isinstance(self.end_date, datetime.datetime):
            return self.published_date <= timezone.now()
        return self.published_date <= timezone.now() <= self.end_date

    def __str__(self):
        """Easy-to-read in shell."""
        return self.question_text


class Choice(models.Model):
    """The Choice model used in polls application. Each choice associate with its question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

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

    def __str__(self):
        """Easy-to-read in shell."""
        return f"Choice: {self.choice.choice_text}, User: {self.user.username}"


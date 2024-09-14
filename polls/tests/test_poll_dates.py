"""Test poll dates related."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from .test_voting import create_question


class QuestionPollDatesTest(TestCase):
    """Test poll dates related."""

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() return False for questions whose published_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(published_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() return False for questions whose published_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(published_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() return True for questions whose published_date is within the
        last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(published_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_published_date(self):
        """
        is_published() return False in this case because it's not been published yet.
        """
        future_question1 = create_question("Future question 1", days=30)
        self.assertIs(future_question1.is_published(), False)
        future_question2 = create_question("Future question 2", seconds=1)
        self.assertIs(future_question2.is_published(), False)

    def test_is_published_with_just_created_question(self):
        """
        is_published() return True in this case because it's already published right now.
        """
        now_question = create_question("now", seconds=0)
        self.assertIs(now_question.is_published(), True)

    def test_is_published_with_past_question(self):
        """
        is_published() return True in this case because it's already published long time ago.
        """
        past_question1 = create_question("Past 1", days=-30)
        past_question2 = create_question("Past 2", seconds=-1)
        self.assertIs(past_question1.is_published(), True)
        self.assertIs(past_question2.is_published(), True)

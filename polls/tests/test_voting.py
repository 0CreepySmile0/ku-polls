"""Test can_vote() method of Question model."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


def create_question(question_text, **kwargs):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(**kwargs)
    return Question.objects.create(question_text=question_text, published_date=time)


class QuestionVotingTest(TestCase):
    """Test can_vote() method of Question model."""

    def test_can_vote_between_published_and_end_date(self):
        """
        can_vote() return True if the question is between the published date and end date.
        """
        pub1 = timezone.now() + datetime.timedelta(days=-30)
        end1 = timezone.now() + datetime.timedelta(days=30)
        question1 = Question.objects.create(question_text="Q1", published_date=pub1, end_date=end1)
        self.assertIs(question1.can_vote(), True)
        pub2 = timezone.now() + datetime.timedelta(seconds=-1)
        end2 = timezone.now() + datetime.timedelta(seconds=1)
        question2 = Question.objects.create(question_text="Q2", published_date=pub2, end_date=end2)
        self.assertIs(question2.can_vote(), True)
        question3 = Question.objects.create(question_text="Q3", published_date=timezone.now())
        self.assertIs(question3.can_vote(), True)

    def test_cannot_vote_before_published_date(self):
        """
        Can't vote before the question is published.
        """
        question1 = create_question("Q1", days=30)
        self.assertIs(question1.can_vote(), False)
        question2 = create_question("Q2", seconds=1)
        self.assertIs(question2.can_vote(), False)

    def test_cannot_vote_after_end_date(self):
        """
        Can't vote after question's end date has passed.
        """
        pub1 = timezone.now() + datetime.timedelta(seconds=-2)
        end1 = timezone.now() + datetime.timedelta(seconds=-1)
        question1 = Question.objects.create(question_text="Q1", published_date=pub1, end_date=end1)
        self.assertIs(question1.can_vote(), False)

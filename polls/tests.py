import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, **kwargs):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(**kwargs)
    return Question.objects.create(question_text=question_text, published_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() return False for questions whose published_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(published_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() return False for questions whose published_date is older than 1 day.
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

    def test_can_vote_between_published_and_end_date(self):
        """
        can_vote() return True if the question is between the published date and end date
        """
        pub1 = timezone.now() + datetime.timedelta(days=-30)
        end1 = timezone.now() + datetime.timedelta(days=30)
        question1 = Question.objects.create(question_text="Q1", published_date=pub1, end_date=end1)
        self.assertIs(question1.can_vote(), True)
        pub2 = timezone.now() + datetime.timedelta(seconds=-1)
        end2 = timezone.now() + datetime.timedelta(seconds=1)
        question2 = Question.objects.create(question_text="Q2", published_date=pub2, end_date=end2)
        self.assertIs(question2.can_vote(), True)
        question3 = Question.objects.create(question_text="Q3", end_date=timezone.now())
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


class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
            ordered=False
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

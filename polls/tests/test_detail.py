"""Test detail page of polls app."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .test_voting import create_question


class QuestionDetailViewTests(TestCase):
    """Test detail page of polls app."""

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        redirect to index page.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.url, '/polls/')

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        user = User.objects.create(username='test1')
        user.set_password('test1')
        user.save()
        self.client.login(username='test1', password='test1')
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

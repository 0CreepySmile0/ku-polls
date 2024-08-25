import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """The Question model use as poll's question in the application"""
    question_text = models.CharField(max_length=200)
    publish_date = models.DateTimeField('date published')

    def was_published_recently(self):
        """Return False if the question was published more than 1 day ago"""
        return self.publish_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        """Easy-to-read in shell"""
        return self.question_text


class Choice(models.Model):
    """The Choice model used in polls application. Each choice associate with its question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Easy-to-read in shell"""
        return self.choice_text

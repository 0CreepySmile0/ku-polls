from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice


class RedirectIndexView(generic.RedirectView):
    """Use to redirect the '/' url to index page"""
    url = "polls/"


class IndexView(generic.ListView):
    """Home page view of polls app that show all available questions"""
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        x = [i.pk for i in Question.objects.all() if i.is_published()]
        return Question.objects.filter(pk__in=x)


class DetailView(generic.DetailView):
    """This view show the question text and all of its choices"""
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        x = [i.pk for i in Question.objects.all() if i.is_published()]
        return Question.objects.filter(pk__in=x)


class ResultsView(generic.DetailView):
    """Show the question text and all vote count of each choice"""
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def check_valid_question(request, pk):
    try:
        get_object_or_404(Question, pk=pk)
        return DetailView.as_view()(request, pk=pk)
    except Http404:
        messages.error(request, "Voting is not allowed for this question or the question doesn't exist")
        return redirect(reverse('polls:index'))

"""Contain request handler view"""
import logging
from mysite import settings
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Question, Choice, Vote


logger = logging.getLogger("polls")


class IndexView(generic.ListView):
    """Home page view of polls app that show all available questions."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(published_date__lte=timezone.now()).\
            order_by('published_date')


class DetailView(LoginRequiredMixin, generic.DetailView):
    """This view show the question text and all of its choices."""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(published_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_vote = Vote.objects.get(user=self.request.user, choice__question=self.object)
            context["user_vote"] = user_vote.choice
        except Vote.DoesNotExist:
            context["user_vote"] = None
        return context


class ResultsView(generic.DetailView):
    """Show the question text and all vote count of each choice."""

    model = Question
    template_name = "polls/results.html"


@login_required
def vote(request, question_id):
    """Vote for a choice on a question (poll)."""

    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if not user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return render(request, "polls/detail.html", {
            "question": question})
    prev_vote = Vote.objects.filter(choice__question=question, user=user)
    if prev_vote:
        prev_vote = prev_vote[0]
        prev_vote.choice = selected_choice
        prev_vote.save()
    else:
        new_vote = Vote.objects.create(user=user, choice=selected_choice)
        new_vote.save()
    messages.info(request, f"Your vote for {selected_choice.choice_text} has been recorded")
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def check_valid_question(request, pk):
    try:
        question = get_object_or_404(Question, pk=pk)
        if question.can_vote():
            return DetailView.as_view()(request, pk=pk)
        messages.error(request, "Voting is not allowed for this question.")
        return redirect(reverse('polls:index'))
    except Http404:
        messages.error(request, "The question doesn't exist")
        return redirect(reverse('polls:index'))
